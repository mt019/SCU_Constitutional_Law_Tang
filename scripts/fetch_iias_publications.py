#!/usr/bin/env python3
"""Fetch and parse IIAS publication listings and downloadable PDFs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
import urllib3
from bs4 import BeautifulSoup


BASE_URL = "https://www.iias.sinica.edu.tw/"
LIST_URL = urljoin(BASE_URL, "publication/0")
PROCESS_URL = urljoin(BASE_URL, "publication_process.php")
DEFAULT_OUT = Path("_Material/研究資料/中研院法律學研究所/出版品總覽")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
)


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = value.replace("\xa0", " ")
    value = re.sub(r"[（(]\s*另開新?視窗\s*[）)]", "", value)
    value = re.sub(r"\bPDF\s*$", "", value, flags=re.I)
    return re.sub(r"\s+", " ", value).strip()


def safe_name(value: str, max_len: int = 90) -> str:
    value = clean_text(value)
    value = re.sub(r"\.PDF$", "", value, flags=re.I)
    value = re.sub(r"\.pdf$", "", value, flags=re.I)
    value = re.sub(r"[\\/:*?\"<>|#%&{}$!`'@+=]", "_", value)
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"_+", "_", value).strip("._ ")
    return (value[:max_len].strip("._ ") or "untitled")


def safe_author(value: str, max_len: int = 50) -> str:
    value = safe_name(value, max_len=max_len)
    value = re.sub(r"(翻譯|審定|譯|編|主編)", "_", value)
    value = re.sub(r"[、，,；;\s]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:max_len].strip("_")


def document_stem(prefix: str, title: str, authors: str = "") -> str:
    author = safe_author(authors)
    title_part = safe_name(title, max_len=90)
    return f"{prefix}_{author}_{title_part}" if author else f"{prefix}_{title_part}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_doc_url(raw_url: str, source_url: str) -> str:
    raw_url = clean_text(raw_url)
    if raw_url.startswith("//"):
        raw_url = "https:" + raw_url
    if raw_url.startswith("publication.iias."):
        raw_url = "https://" + raw_url
    url = urljoin(source_url, raw_url)
    parsed = urlparse(url)
    if parsed.netloc == "publication.iias.tw":
        url = parsed._replace(scheme="https", netloc="publication.iias.sinica.edu.tw").geturl()
    return url


@dataclass
class Fetcher:
    out_dir: Path
    delay: float = 0.15
    force: bool = False

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.raw_dir = self.out_dir / "raw_html"
        self.items_dir = self.out_dir / "items"
        self.pdf_dir = self.out_dir / "pdf"
        self.text_dir = self.out_dir / "pdf_text"
        self.html_doc_dir = self.out_dir / "html_docs"
        self.html_text_dir = self.out_dir / "html_text"
        self.parsed_dir = self.out_dir / "_parsed"
        for d in [self.raw_dir, self.items_dir, self.pdf_dir, self.text_dir, self.html_doc_dir, self.html_text_dir, self.parsed_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def get(self, url: str) -> requests.Response:
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        time.sleep(self.delay)
        return response

    def post(self, url: str, data: dict[str, Any]) -> requests.Response:
        response = self.session.post(url, data=data, timeout=60)
        response.raise_for_status()
        time.sleep(self.delay)
        return response

    def fetch_listing(self) -> list[dict[str, Any]]:
        html = self.get(LIST_URL).text
        (self.raw_dir / "publication_0.html").write_text(html, encoding="utf-8")
        token_match = re.search(r"'X_CSRF_TOKEN':\s*'([0-9a-f]+)'", html)
        if not token_match:
            raise RuntimeError("Could not find IIAS CSRF token in listing page")
        token = token_match.group(1)

        articles: list[dict[str, Any]] = []
        seen: set[str] = set()
        offset = 0
        limit = 15
        total = None
        while True:
            payload = {
                "X_CSRF_TOKEN": token,
                "acId": 0,
                "acTitle": "",
                "offset": offset,
                "limit": limit,
            }
            data = self.post(PROCESS_URL, payload).json()
            if total is None:
                total = int(data.get("total", 0))
            batch = data.get("articles") or []
            if not batch:
                break
            for row in batch:
                url = urljoin(BASE_URL, row["url"])
                if url in seen:
                    continue
                seen.add(url)
                row = dict(row)
                row["url"] = url
                row["source_list_url"] = LIST_URL
                articles.append(row)
            offset = 15 if offset == 0 else offset + 8
            limit = 8
            if len(articles) >= total:
                break
        return articles

    def parse_detail(self, article: dict[str, Any]) -> dict[str, Any]:
        source_url = article["url"]
        parts = [p for p in urlparse(source_url).path.split("/") if p]
        post_id = parts[1] if len(parts) > 1 else hashlib.sha1(source_url.encode()).hexdigest()[:8]
        category_id = parts[2] if len(parts) > 2 else ""
        stem = f"{post_id}_{safe_name(article.get('title') or '')}"

        html_path = self.raw_dir / f"{stem}.html"
        if self.force or not html_path.exists():
            html = self.get(source_url).text
            html_path.write_text(html, encoding="utf-8")
        else:
            html = html_path.read_text(encoding="utf-8")

        soup = BeautifulSoup(html, "html.parser")
        info = soup.select_one(".publication-info")
        content = soup.select_one(".publication-content")
        text_block = soup.select_one(".text-block")

        metadata: dict[str, str] = {}
        if info:
            for li in info.select("li"):
                spans = li.find_all("span")
                if not spans:
                    continue
                labels = [clean_text(s.get_text(" ")) for s in spans]
                full = clean_text(li.get_text(" "))
                for label in labels:
                    full = full.replace(label, f" {label}: ", 1)
                for part in re.split(r"\s{2,}|(?=\S+[:：])", full):
                    if ":" in part:
                        k, v = part.split(":", 1)
                    elif "：" in part:
                        k, v = part.split("：", 1)
                    else:
                        continue
                    k, v = clean_text(k), clean_text(v)
                    if k and v and k not in {"Facebook icon", "Line icon", "Twitter icon"}:
                        metadata[k] = v

        title = clean_text((info.select_one("h1") if info else None).get_text(" ") if info and info.select_one("h1") else article.get("title", ""))
        description = clean_text((info.select_one("p") if info else None).get_text(" ") if info and info.select_one("p") else article.get("content", ""))
        cover = ""
        if info and info.select_one("img"):
            cover = urljoin(BASE_URL, info.select_one("img").get("src", ""))

        chapters: list[dict[str, Any]] = []
        current_section = ""
        if content:
            for node in content.find_all(["h2", "div"], recursive=True):
                if node.name == "h2" and not node.find_parent(class_="chapter"):
                    current_section = clean_text(node.get_text(" "))
                    continue
                classes = node.get("class") or []
                if node.name != "div" or "chapter" not in classes:
                    continue
                heading = node.select_one("h3") or node.select_one("h2")
                chapter_title = clean_text(heading.get_text(" ")) if heading else ""
                chapter: dict[str, Any] = {
                    "section": current_section,
                    "title": chapter_title,
                    "authors": "",
                    "page_range": "",
                    "download_url": "",
                    "download_title": "",
                }
                for li in node.select("ul.author li"):
                    text = clean_text(li.get_text(" "))
                    if "作者" in text:
                        chapter["authors"] = clean_text(text.replace("作者", ""))
                    elif "頁碼" in text:
                        chapter["page_range"] = clean_text(text.replace("頁碼", ""))
                    elif text:
                        chapter.setdefault("notes", []).append(text)
                link = node.select_one("ul.download a[href]")
                if link:
                    chapter["download_url"] = normalize_doc_url(link["href"], source_url)
                    chapter["download_title"] = clean_text(link.get("title") or link.get_text(" "))
                chapters.append(chapter)

        extra_text = clean_text(text_block.get_text("\n")) if text_block else ""
        parsed = {
            "post_id": post_id,
            "category_id": category_id,
            "title": title,
            "category": article.get("acTitle", ""),
            "date": article.get("date", ""),
            "source_url": source_url,
            "list_summary": clean_text(article.get("content", "")),
            "description": description,
            "cover_url": cover or article.get("photo", ""),
            "metadata": metadata,
            "chapters": chapters,
            "extra_text": extra_text,
            "raw_html": str(html_path.relative_to(self.out_dir)),
        }
        return parsed

    def download_pdf(self, url: str, title: str, prefix: str, authors: str = "") -> dict[str, Any]:
        pdf_name = f"{document_stem(prefix, title, authors)}.pdf"
        pdf_path = self.pdf_dir / pdf_name
        text_path = self.text_dir / f"{pdf_path.stem}.txt"
        error = ""

        if self.force or not pdf_path.exists():
            try:
                response = self.get(url)
                pdf_path.write_bytes(response.content)
            except Exception as exc:  # noqa: BLE001
                error = f"download_error: {exc}"

        pages = None
        text_chars = 0
        if pdf_path.exists() and not error:
            try:
                info = subprocess.run(
                    ["pdfinfo", str(pdf_path)],
                    check=False,
                    text=True,
                    capture_output=True,
                )
                m = re.search(r"^Pages:\s+(\d+)", info.stdout, flags=re.M)
                pages = int(m.group(1)) if m else None
                if self.force or not text_path.exists():
                    subprocess.run(
                        ["pdftotext", "-layout", str(pdf_path), str(text_path)],
                        check=False,
                        text=True,
                        capture_output=True,
                    )
                if text_path.exists():
                    text_chars = len(text_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception as exc:  # noqa: BLE001
                error = f"parse_error: {exc}"

        return {
            "download_url": url,
            "document_type": "pdf",
            "pdf_path": str(pdf_path.relative_to(self.out_dir)) if pdf_path.exists() else "",
            "text_path": str(text_path.relative_to(self.out_dir)) if text_path.exists() else "",
            "sha256": sha256_file(pdf_path) if pdf_path.exists() else "",
            "pdf_pages": pages,
            "text_chars": text_chars,
            "error": error,
        }

    def fetch_html_document(self, url: str, title: str, prefix: str, authors: str = "") -> dict[str, Any]:
        doc_dir = self.html_doc_dir / document_stem(prefix, title, authors)
        doc_dir.mkdir(parents=True, exist_ok=True)
        index_path = doc_dir / "index.html"
        text_path = self.html_text_dir / f"{doc_dir.name}.txt"
        error = ""
        page_count = 0
        page_paths: list[str] = []
        image_urls: list[str] = []
        text_parts: list[str] = []

        try:
            index_html = self.get(url).text
            index_path.write_text(index_html, encoding="utf-8")
            index_soup = BeautifulSoup(index_html, "html.parser")
            title_text = clean_text(index_soup.title.get_text(" ")) if index_soup.title else title
            text_parts.append(f"# {title_text}")

            pages_js_url = urljoin(url, "javascript/pages.js")
            pages_js = self.get(pages_js_url).text
            (doc_dir / "pages.js").write_text(pages_js, encoding="utf-8")
            page_names = re.findall(r'"item"\s*:\s*"([^"]+)"', pages_js)
            page_names = [p for p in page_names if p.startswith("page")]
            if not page_names:
                m = re.search(r'id="lastPage"[^>]*>\s*/\s*(\d+)', index_html)
                page_names = [f"page{i}" for i in range(1, int(m.group(1)) + 1)] if m else []
            page_count = len(page_names)

            toc_url = urljoin(url, "toc.html")
            toc_html = self.get(toc_url).text
            (doc_dir / "toc.html").write_text(toc_html, encoding="utf-8")
            toc_soup = BeautifulSoup(toc_html, "html.parser")
            toc_text = clean_text(toc_soup.get_text("\n"))
            if toc_text:
                text_parts += ["", "## TOC", toc_text]

            for page_name in page_names:
                page_url = urljoin(url, f"{page_name}.html")
                page_html = self.get(page_url).text
                page_path = doc_dir / f"{page_name}.html"
                page_path.write_text(page_html, encoding="utf-8")
                page_paths.append(str(page_path.relative_to(self.out_dir)))

                page_soup = BeautifulSoup(page_html, "html.parser")
                for img in page_soup.select("img[src]"):
                    src = img.get("src") or ""
                    if "page" in src.lower():
                        image_urls.append(urljoin(page_url, src))
                for tag in page_soup(["script", "style", "nav", "img"]):
                    tag.decompose()
                page_text = clean_text(page_soup.get_text("\n"))
                if page_text:
                    text_parts += ["", f"## {page_name}", page_text]
        except Exception as exc:  # noqa: BLE001
            error = f"html_fetch_error: {exc}"

        text_path.write_text("\n".join(text_parts).rstrip() + "\n", encoding="utf-8")
        return {
            "download_url": url,
            "document_type": "html",
            "html_dir": str(doc_dir.relative_to(self.out_dir)),
            "html_index": str(index_path.relative_to(self.out_dir)),
            "text_path": str(text_path.relative_to(self.out_dir)),
            "html_page_count": page_count,
            "html_pages": page_paths,
            "image_urls": sorted(set(image_urls)),
            "text_chars": len(text_path.read_text(encoding="utf-8", errors="ignore")) if text_path.exists() else 0,
            "error": error,
        }

    def fetch_document(self, url: str, title: str, prefix: str, authors: str = "") -> dict[str, Any]:
        if ".pdf" in urlparse(url).path.lower():
            return self.download_pdf(url, title, prefix, authors)
        return self.fetch_html_document(url, title, prefix, authors)

    def write_item_files(self, item: dict[str, Any]) -> None:
        stem = f"{item['post_id']}_{safe_name(item['title'])}"
        json_path = self.items_dir / f"{stem}.json"
        md_path = self.items_dir / f"{stem}.md"
        json_path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")

        lines = [
            f"# {item['title']}",
            "",
            f"- 類別：{item['category']}",
            f"- 出版年月：{item['date']}",
            f"- 原始頁面：{item['source_url']}",
        ]
        for k, v in item["metadata"].items():
            lines.append(f"- {k}：{v}")
        if item["description"]:
            lines += ["", "## 摘要", "", item["description"]]
        if item["chapters"]:
            lines += ["", "## 總目錄"]
            for chapter in item["chapters"]:
                lines += [
                    "",
                    f"### {chapter.get('title') or '未題名'}",
                    "",
                    f"- 分類：{chapter.get('section', '')}",
                    f"- 作者：{chapter.get('authors', '')}",
                    f"- 頁碼：{chapter.get('page_range', '')}",
                    f"- PDF：{chapter.get('download_url', '')}",
                    f"- 文字檔：{chapter.get('text_path', '')}",
                ]
        if item["extra_text"]:
            lines += ["", "## 其他文字", "", item["extra_text"]]
        md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    def run(self) -> dict[str, Any]:
        articles = self.fetch_listing()
        items: list[dict[str, Any]] = []
        pdf_count = 0
        html_count = 0
        for idx, article in enumerate(articles, start=1):
            item = self.parse_detail(article)
            for chap_idx, chapter in enumerate(item["chapters"], start=1):
                url = chapter.get("download_url")
                if not url:
                    continue
                prefix = f"{item['post_id']}_{chap_idx:02d}"
                doc_meta = self.fetch_document(url, chapter.get("title") or chapter.get("download_title") or "fulltext", prefix, chapter.get("authors", ""))
                chapter.update(doc_meta)
                pdf_count += doc_meta.get("document_type") == "pdf" and bool(doc_meta.get("pdf_path"))
                html_count += doc_meta.get("document_type") == "html" and bool(doc_meta.get("html_index"))
            self.write_item_files(item)
            items.append(item)
            print(f"[{idx}/{len(articles)}] {item['title']} ({len(item['chapters'])} chapters)")

        manifest = {
            "source": LIST_URL,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "publication_count": len(items),
            "pdf_count": int(pdf_count),
            "html_doc_count": int(html_count),
            "items": items,
        }
        (self.out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        self.write_tables(items)
        return manifest

    def write_tables(self, items: list[dict[str, Any]]) -> None:
        pub_csv = self.parsed_dir / "publications.csv"
        chapter_csv = self.parsed_dir / "chapters.csv"
        with pub_csv.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=["post_id", "title", "category", "date", "source_url", "chapter_count", "pdf_count", "html_doc_count", "description"],
            )
            writer.writeheader()
            for item in items:
                writer.writerow(
                    {
                        "post_id": item["post_id"],
                        "title": item["title"],
                        "category": item["category"],
                        "date": item["date"],
                        "source_url": item["source_url"],
                        "chapter_count": len(item["chapters"]),
                        "pdf_count": sum(1 for c in item["chapters"] if c.get("pdf_path")),
                        "html_doc_count": sum(1 for c in item["chapters"] if c.get("html_index")),
                        "description": item["description"] or item["list_summary"],
                    }
                )
        with chapter_csv.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=[
                    "post_id",
                    "publication_title",
                    "publication_date",
                    "category",
                    "section",
                    "chapter_title",
                    "authors",
                    "page_range",
                    "download_url",
                    "document_type",
                    "pdf_path",
                    "html_index",
                    "text_path",
                    "pdf_pages",
                    "html_page_count",
                    "text_chars",
                    "error",
                ],
            )
            writer.writeheader()
            for item in items:
                for chapter in item["chapters"]:
                    writer.writerow(
                        {
                            "post_id": item["post_id"],
                            "publication_title": item["title"],
                            "publication_date": item["date"],
                            "category": item["category"],
                            "section": chapter.get("section", ""),
                            "chapter_title": chapter.get("title", ""),
                            "authors": chapter.get("authors", ""),
                            "page_range": chapter.get("page_range", ""),
                            "download_url": chapter.get("download_url", ""),
                            "document_type": chapter.get("document_type", ""),
                            "pdf_path": chapter.get("pdf_path", ""),
                            "html_index": chapter.get("html_index", ""),
                            "text_path": chapter.get("text_path", ""),
                            "pdf_pages": chapter.get("pdf_pages", ""),
                            "html_page_count": chapter.get("html_page_count", ""),
                            "text_chars": chapter.get("text_chars", ""),
                            "error": chapter.get("error", ""),
                        }
                    )

        by_category: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            by_category.setdefault(item["category"] or "未分類", []).append(item)
        lines = [
            "# 中央研究院法律學研究所出版品總覽",
            "",
            f"- 來源：{LIST_URL}",
            f"- 抓取時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- 出版品筆數：{len(items)}",
            f"- 章節/篇目筆數：{sum(len(i['chapters']) for i in items)}",
            f"- PDF 筆數：{sum(1 for i in items for c in i['chapters'] if c.get('pdf_path'))}",
            f"- HTML 線上閱覽文件筆數：{sum(1 for i in items for c in i['chapters'] if c.get('html_index'))}",
            "",
            "## 檔案結構",
            "",
            "- `raw_html/`：列表頁與逐篇出版品頁面的原始 HTML",
            "- `items/`：逐篇出版品 JSON 與 Markdown",
            "- `pdf/`：下載的 PDF 原檔",
            "- `pdf_text/`：由 `pdftotext -layout` 解析出的文字",
            "- `html_docs/`：早期線上閱覽版 HTML 文件包",
            "- `html_text/`：由 HTML 文件包抽出的目錄與文字層",
            "- `_parsed/publications.csv`：出版品層級總表",
            "- `_parsed/chapters.csv`：篇章/文件層級總表",
            "- `manifest.json`：完整結構化資料與檔案指紋",
            "",
            "## 分類索引",
        ]
        for category, rows in sorted(by_category.items()):
            lines += ["", f"### {category}"]
            for item in rows:
                lines.append(f"- {item['date']} [{item['title']}](items/{item['post_id']}_{safe_name(item['title'])}.md)（{len(item['chapters'])} 篇）")
        (self.out_dir / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--delay", type=float, default=0.15)
    args = parser.parse_args()

    fetcher = Fetcher(args.out_dir, delay=args.delay, force=args.force)
    manifest = fetcher.run()
    print(json.dumps({"publication_count": manifest["publication_count"], "pdf_count": manifest["pdf_count"], "html_doc_count": manifest["html_doc_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

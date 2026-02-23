# Dockerfile（正確版）
FROM squidfunk/mkdocs-material:latest

# 可選：升級 pip，避免舊版相依問題
RUN pip install --no-cache-dir -U pip

# 一次安裝所有外掛與擴展
RUN pip install --no-cache-dir \
    mkdocs-awesome-pages-plugin \
    mkdocs-exclude \
    mkdocs-minify-plugin \
    mkdocs-git-revision-date-localized-plugin \
    mdx_truly_sane_lists
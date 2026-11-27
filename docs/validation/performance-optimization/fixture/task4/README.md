# blog-publisher

Command-line publisher the editors use for the company blog.

- `blog/slug.py`: `slugify(title)` turns an article title into its URL slug.
- `blog/publish.py`: `python -m blog.publish ARTICLE.md [--dry-run]` builds the slug, renders
  the article and uploads it with its images to the CDN. It prints how long each step took.
- `python -m unittest` runs the tests.

Editors publish about 40 articles a day. Slugs must stay stable: an existing article's slug is
its public URL.

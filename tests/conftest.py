# this package
from searchdocs import cache_dir_for_url
from searchdocs.__main__ import DOCS_PYTHON_ORG

(cache_dir_for_url(DOCS_PYTHON_ORG) / "cache.db").unlink(missing_ok=True)

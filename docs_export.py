import os
from config import DOCS_HTML_DIR

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{
    font-family: system-ui;
    max-width: 900px;
    margin: auto;
    padding: 2rem;
}}
</style>
</head>
<body>{content}</body>
</html>
"""

def export_html(step_name, content, doc_type):
    os.makedirs(DOCS_HTML_DIR, exist_ok=True)

    html = HTML_TEMPLATE.format(
        title=f"{step_name} — {doc_type}",
        content=content.replace("\n", "<br>")
    )

    path = f"{DOCS_HTML_DIR}/{step_name}_{doc_type}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    return path
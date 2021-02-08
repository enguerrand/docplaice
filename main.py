import os

import markdown
from flask import Flask, render_template, abort
from pathlib import Path

import config

app = Flask(__name__)


def render_markdown(path, md_root):
    requested_path = os.path.join(md_root, path)
    if os.path.isdir(requested_path):
        return render_dir(requested_path, md_root)
    elif path.endswith(".md"):
        return render_file(requested_path)
    else:
        return None


def render_dir(directory, md_root):
    children = os.listdir(directory)
    current_path = directory.replace(md_root, "/")
    if not current_path.endswith("/"):
        current_path = current_path + "/"
    if current_path == "/":
        return render_template("toc.html", current_path=current_path, children=children)
    else:
        path = Path(directory.replace(md_root, "/"))
        up = str(path.parent)
        if not up.endswith("/"):
            up = up + "/"
        return render_template("toc.html", current_path=current_path, children=children, up=up)


def render_file(md_file):
    try:
        with open(md_file, 'r') as file:
            md = file.read()
    except:
        return None
    html = markdown.markdown(md, extensions=['extra'])
    return render_template("page.html", title="edrwiki", rendered_markdown=html)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    md_root = config.markdown_root
    if not md_root.endswith("/"):
        md_root = md_root + "/"
    rendered_md = render_markdown(path, md_root)
    if rendered_md is None:
        abort(404)
    else:
        return rendered_md


if __name__ == '__main__':
    app.run()
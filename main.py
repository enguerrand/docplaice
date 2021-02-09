import os
import re

import markdown
from flask import Flask, render_template, abort, send_from_directory

import config

app = Flask(__name__)


class Page:
    def __init__(self, title, url, level):
        self.title = title
        self.url = url
        self.level = level


def render_page(path, md_root):
    requested_path = os.path.join(md_root, path)
    directory = os.path.isdir(requested_path)
    new_current_path, breadcrumbs = build_breadcrumbs(requested_path.replace(md_root, ""), directory)

    if directory:
        html = render_dir(requested_path, new_current_path)
    elif path.endswith(".md"):
        html = render_file(requested_path)
    else:
        html = None
    if html is None:
        return None
    else:
        return render_template(
            "page.html",
            breadcrumbs=breadcrumbs,
            title=breadcrumbs[-1].title,
            rendered_content=html,
            theme=config.theme,
        )


def build_breadcrumbs(path_to_page, add_slash_to_last):
    current_path = re.sub("/$", "", path_to_page)
    current_path = re.sub("^/", "", current_path)
    breadcrumb_url = "/"
    breadcrumb_depth = 0
    breadcrumbs = [Page("Home", breadcrumb_url, breadcrumb_depth)]
    if current_path != "":
        tokens = current_path.split("/")
        for token in tokens:
            breadcrumb_depth = breadcrumb_depth + 1
            breadcrumb_url = breadcrumb_url + token + "/"
            breadcrumbs.append(Page(token, breadcrumb_url, breadcrumb_depth))
        if not add_slash_to_last:
            breadcrumbs[-1].url = breadcrumbs[-1].url.removesuffix("/")
        current_path = current_path + "/"
    current_path = "/" + current_path
    return current_path, breadcrumbs


def render_dir(directory, current_path):
    subdirs, pages = list_children_ordered(directory)

    return render_template(
        "toc.html",
        current_path=current_path,
        subdirs=subdirs,
        pages=pages,
        theme=config.theme,
    )


def list_children_ordered(parent):
    children = os.listdir(parent)
    children.sort()
    dirs = []
    files = []
    for child in children:
        if os.path.isdir(os.path.join(parent, child)):
            dirs.append(child)
        else:
            files.append(child)
    return dirs, files


def render_file(md_file):
    try:
        with open(md_file, "r") as file:
            md = file.read()
    except:
        return None
    return markdown.markdown(md, extensions=["extra"])


@app.route("/css/<path:path>")
def send_js(path):
    return send_from_directory("css", path)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    md_root = config.markdown_root
    if not md_root.endswith("/"):
        md_root = md_root + "/"
    rendered_page = render_page(path, md_root)
    if rendered_page is None:
        abort(404)
    else:
        return rendered_page


def kwargs_printer(**kwargs):
    print(kwargs)


if __name__ == "__main__":
    app.run()
    # my_args = {"foo": "bar"}
    # kwargs_printer(**my_args)

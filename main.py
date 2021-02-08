import os
import re

import markdown
from flask import Flask, render_template, abort, send_from_directory

import config

app = Flask(__name__)


def render_markdown(path, md_root):
    requested_path = os.path.join(md_root, path)
    directory = os.path.isdir(requested_path)
    new_current_path, new_current_path_tokens = tokenize_path(requested_path.replace(md_root, ""), directory)

    if directory:
        return render_dir(requested_path, new_current_path, new_current_path_tokens)
    elif path.endswith(".md"):
        return render_file(requested_path, new_current_path, new_current_path_tokens)
    else:
        return None


def tokenize_path(path_to_tokenize, add_slash_to_last):
    current_path = re.sub("/$", "", path_to_tokenize)
    current_path = re.sub("^/", "", current_path)
    current_path_tokens = ["/"]
    if current_path != "":
        tokens = current_path.split("/")
        for token in tokens:
            current_path_tokens.append(token + "/")
        if not add_slash_to_last:
            current_path_tokens[-1] = current_path_tokens[-1].removesuffix("/")
        current_path = current_path + "/"
    current_path = "/" + current_path
    return current_path, current_path_tokens


def render_dir(directory, current_path, current_path_tokens):
    subdirs, pages = list_children_ordered(directory)

    return render_template(
        "toc.html",
        current_path=current_path,
        current_path_tokens=current_path_tokens,
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


def render_file(md_file, current_path, current_path_tokens):
    try:
        with open(md_file, "r") as file:
            md = file.read()
    except:
        return None
    html = markdown.markdown(md, extensions=["extra"])
    return render_template(
        "page.html",
        current_path=current_path,
        current_path_tokens=current_path_tokens,
        title="edrwiki",
        rendered_markdown=html,
        theme=config.theme,
    )


@app.route("/css/<path:path>")
def send_js(path):
    return send_from_directory("css", path)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    md_root = config.markdown_root
    if not md_root.endswith("/"):
        md_root = md_root + "/"
    rendered_md = render_markdown(path, md_root)
    if rendered_md is None:
        abort(404)
    else:
        return rendered_md


def kwargs_printer(**kwargs):
    print(kwargs)


if __name__ == "__main__":
    app.run()
    # my_args = {"foo": "bar"}
    # kwargs_printer(**my_args)

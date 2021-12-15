import os
import re
import sys, traceback

import markdown
from flask import Flask, Response, render_template, abort, send_from_directory
from werkzeug.utils import redirect

import config

REGEX_MD_EXT = "\\.md$"
REGEX_PATH_WHITELIST = "^[0-9a-zA-Z/_\\-]*$"

app = Flask(__name__)


class Page:
    def __init__(self, title, url, level, current=False):
        self.title = title
        self.url = url
        self.level = level
        self.current = current


def render_page(path, md_root):
    try:
        return render_page_unsafe(path, md_root)
    except:
        traceback.print_exception(*sys.exc_info())
        return None


def render_page_unsafe(path, md_root):
    requested_path = os.path.join(md_root, path)
    directory = os.path.isdir(requested_path)

    if directory and not path.endswith("/") and path != "":
        return redirect(path + "/", code=301)

    new_current_path, breadcrumbs = build_breadcrumbs(requested_path.replace(md_root, ""), directory)

    if directory:
        current_section = new_current_path
    else:
        current_section = os.path.dirname(to_canonical_relative_path(new_current_path))
    side_bar_navigation = build_sidebar_navigation(md_root, current_section)

    if directory:
        possible_index = os.path.join(requested_path, "index.md")
        html = ""
        if os.path.exists(possible_index):
            html = html + render_file(possible_index) + "\n"
        html = html + render_dir(requested_path, new_current_path, breadcrumbs[-1].title)
    else:
        if path.endswith(".md"):
            html = render_file(requested_path)
        else:
            html = render_file(requested_path + ".md")
    if html is None:
        return None
    else:
        search_index = build_search_index(config.search_type, md_root)
        return render_template(
            "page.html",
            wiki_name=config.wiki_name,
            side_bar_navigation=side_bar_navigation,
            breadcrumbs=breadcrumbs,
            title=breadcrumbs[-1].title,
            rendered_content=html,
            theme=config.theme,
            search_index=search_index
        )


def build_sidebar_navigation(md_root, path_to_page):
    here = to_canonical_relative_path(path_to_page)
    side_bar_navigation = [Page("home", "/", 0, here == "")]
    for root, dirs, files in os.walk(md_root, followlinks=True):
        stripped_root = strip_root(md_root, root)
        depth = stripped_root.count(os.sep)
        for name in dirs:
            url = os.path.join(stripped_root, name) + "/"
            if contains_forbidden_chars(url):
                continue
            page = Page(name, url, depth, here == to_canonical_relative_path(url))
            side_bar_navigation.append(page)
    side_bar_navigation.sort(key=lambda page: page.url)
    return side_bar_navigation


def build_page(depth, name, root):
    url = os.path.join(root, name)
    page = Page(name, url, depth)
    return page


def build_breadcrumbs(path_to_page, add_slash_to_last):
    current_path = to_canonical_relative_path(path_to_page)
    breadcrumb_url = "/"
    breadcrumb_depth = 0
    breadcrumbs = [Page(config.wiki_name, breadcrumb_url, breadcrumb_depth)]
    if current_path != "":
        tokens = current_path.split("/")
        for token in tokens:
            breadcrumb_depth = breadcrumb_depth + 1
            breadcrumb_url = breadcrumb_url + token + "/"
            breadcrumbs.append(Page(token, breadcrumb_url, breadcrumb_depth))
        if not add_slash_to_last:
            breadcrumbs[-1].url = remove_trailing_slash(breadcrumbs[-1].url)
        current_path = current_path + "/"
    current_path = "/" + current_path
    return current_path, breadcrumbs


def to_canonical_relative_path(path_to_page):
    removed_trailing = re.sub("/$", "", path_to_page)
    removed_leading = re.sub("^/", "", removed_trailing)
    return removed_leading


def render_dir(directory, current_path, section_title):
    children = os.listdir(directory)
    children.sort()
    pages = []
    for child in children:
        if starts_with_dot(child):
            continue
        if child == "index.md":
            continue
        if not os.path.isfile(os.path.join(directory, child)):
            continue
        page_name = re.sub(REGEX_MD_EXT, "", child)
        pages.append(page_name)

    if len(pages) == 0:
        return ""
    return render_template(
        "toc.html",
        title=section_title,
        current_path=current_path,
        pages=pages,
        theme=config.theme,
    )


def render_file(md_file):
    try:
        with open(md_file, "r", encoding="UTF-8") as file:
            md = file.read()
    except:
        traceback.print_exception(*sys.exc_info())
        return None
    return markdown.markdown(md, extensions=["extra"])


def build_search_index(search_type, md_root):
    if search_type == "page-name":
        search_index = {}
        for root, dirs, files in os.walk(md_root, followlinks=True):
            stripped_root = strip_root(md_root, root)
            for name in files:
                if name == "index.md":
                    continue
                url = os.path.join(stripped_root, name)
                if contains_forbidden_chars(url):
                    continue
                try:
                    matches = search_index[name]
                except KeyError:
                    matches = []
                    search_index[name] = matches
                matches.append({
                    "name": re.sub(REGEX_MD_EXT, "", name),
                    "url": url
                })
        return search_index
    else:
        return None


def strip_root(md_root, relative_to):
    stripped_root = relative_to.replace(md_root, "/")
    if stripped_root != "/" and not stripped_root.endswith("/"):
        stripped_root = stripped_root + "/"
    return stripped_root


def remove_trailing_slash(input):
    return re.sub("/$", "", input)


def contains_forbidden_chars(path):
    stripped_md_ext = re.sub(REGEX_MD_EXT, "", path)
    if re.compile(REGEX_PATH_WHITELIST).match(stripped_md_ext):
        return False
    return True


def starts_with_dot(char_sequence):
    return re.compile('^\\..*').match(char_sequence)


@app.route("/css/style.css")
def css():
    return Response(render_template("style.css", theme=config.theme), mimetype="text/css")


@app.route("/img/docplaice.svg")
def svg():
    return Response(render_template("docplaice.svg", theme=config.theme), mimetype="image/svg+xml")


@app.route("/assets/<path:path>")
def serve_assets(path):
    return send_from_directory("assets", path)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    if contains_forbidden_chars(path):
        print(f"Sending 404 because of forbidden chars in {path}")
        abort(404)

    md_root = config.markdown_root
    if not md_root.endswith("/"):
        md_root = md_root + "/"
    rendered_page = render_page(path, md_root)
    if rendered_page is None:
        print(f"Sending 404 because of requested path was not found")
        abort(404)
    else:
        return rendered_page


if __name__ == "__main__":
    app.run()

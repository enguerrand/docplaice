import os

import markdown
from flask import Flask, render_template

import config

app = Flask(__name__)


def render_markdown(path):
    md_file = os.path.join(config.markdown_root, path)
    try:
        with open(md_file, 'r') as file:
            md = file.read()
    except:
        md = ""
    html = markdown.markdown(md, extensions=['extra'])
    return html


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    rendered_md = render_markdown(path)
    return render_template("index.html", title="edrwiki", rendered_markdown=rendered_md)


if __name__ == '__main__':
    app.run()
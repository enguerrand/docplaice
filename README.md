# docplaice
A Place for flat File Documentation

## Description
Docplaice is a webservice written in python that dynamically renders markdown files as html. 

If you want to take a look at Docplaice in action feel free to visit [my own installation](https://wiki.rochefort.de). 

It is based on the [Flask](https://palletsprojects.com/p/flask/) web framework.

## License
Docplaice is licensed under the [GPL, version 3](LICENSE).

For the python dependencies different licensing may apply, please refer to the documentation of the individual projects.
You can find a complete list of these projects in the [requirements file](requirements.txt).

The [bootstrap css](https://getbootstrap.com/) file contained in this repository contains the relevant licensing information inline.

The search field uses [reactjs](https://reactjs.org/) licensed under the [MIT license](https://github.com/facebook/react/blob/master/LICENSE).

The provided colorschemes are using
[Ethan Schoonover's awesome solarized theme](https://ethanschoonover.com/solarized/), the license of which 
can be found on the project's [github repo](https://github.com/altercation/solarized/blob/master/LICENSE)    

## Installation
I used the commands listed below to get docplaice up and running with apache. 
They are not meant for simple copy/paste... think before you execute them on your machine!

Run as root:
```bash
apt install virtualenv git
mkdir -p /opt/venvs
cd /opt/venvs
git clone https://github.com/enguerrand/docplaice.git
cd docplaice
mkdir venv
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Now configure docplaice as a wsgi application in your webserver. 
Please refer to your webserver's documentation on how to do this exactly.
The [flask documentation](https://flask.palletsprojects.com/en/1.1.x/deploying/) for deployment is 
a good resource for this task as well.

Note that this repository contains the wsgi file that works for me in combination with apache.

## Configuration
The configuration for docplaice takes place in the config.py that ships with this repo.
The single-most important setting in this file is the "markdown_root" entry.
This must point to the path where your markdown files are located.

## Markdown root organisation
Docplaice supports structuring your documents using the following logic:

Each directory is considered a category and will get an entry in the sidebar menu. 
The depth in the directory structure is visualised by indenting the buttons accordingly.

The current location is also visualized using a breadcrumb navigation on the top of the page.

Request URLs are processed in the following way:

* The relative path fraction of the url is added to the configured document root
* If the resulting path points at a markdown file, that file is rendered
* If needed, the extension .md is appended to the provided url to find an existing markdown file
* If the path points to a directory, a list of markdown files in the given directory is rendered
* If the directory contains a file named index.md, that file is rendered above said list of files  

## Upgrading
In order to upgrade your installation, you can simply
```bash
git pull
```
You then may have to reload/restart your webserver. E.g. on Debian/apache:
```bash
systemctl reload apache2
```

## Tips
If you add links between your pages in the markdown files, use relative links.
This way you can jump to the linked file from within your editor if your editor supports this.

E.g. in vim, the command for this is gf (as in "goto file")

activate_this = '/opt/venvs/docplaice/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import logging
import sys

sys.path.insert(0, '/opt/venvs/docplaice/')

logging.basicConfig(stream=sys.stderr)
from main import app as application


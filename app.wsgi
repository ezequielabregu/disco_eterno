import sys
sys.path.insert(0, '/var/www/html/apps/disco_eterno')

#activate_this = '/var/www/html/apps/polybuzz/venv/bin/activate_this.py'
#with open(activate_this) as file:
#    exec(file.read(), dict(__file__=activate_this))

from app import app as application

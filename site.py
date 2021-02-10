# Tutorial
# https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
import os
import sys
from app.load import get_global
from app.write import generate_site
from app.server import run
from app.helpers import tailwind_os


# Returns site.person, site.settings
site = get_global()
# Generate HTML site
generate_site(site)

# Compile CSS for production
if 'compile' in sys.argv:
    os.system(tailwind_os('compile'))

# Run dev server with full Tailwind CSS
if 'server' in sys.argv:
    os.system(tailwind_os())
    run()

# Watch for changes
if 'watch' in sys.argv:
    exec(open("./app/watch.py").read())

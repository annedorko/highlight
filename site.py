# Tutorial
# https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
import os
import sys
from app.load import get_global
from app.write import generate_site
from app.server import run
from app.helpers import tailwind_os

# Set global variables, prepare compile
if 'compile' in sys.argv:
    site = get_global(compile=True)
    generate_site(site)
    os.system(tailwind_os('compile'))
else:
    site = get_global()
    # Generate HTML site
    generate_site(site)
    os.system(tailwind_os())

# Run dev server with full Tailwind CSS
if 'server' in sys.argv:
    os.system(tailwind_os())
    run()

# Watch for changes
if 'watch' in sys.argv:
    exec(open("./app/watch.py").read())

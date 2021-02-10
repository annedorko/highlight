# Tutorial
# https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
import os
import sys
from app.load import get_global
from app.write import RegenerateSite, generate_site
import time
import logging
from watchdog.observers import Observer
from app.server import run


# Returns site.person, site.settings
site = get_global()
# Generate HTML site
generate_site(site)

# Compile CSS for production
if 'compile' in sys.argv:
    os.system(
        'npx tailwind build ./assets/css/styles.css -o site/assets/css/styles.css -c tailwind.prod.config.js')

# Run dev server with full Tailwind CSS
if 'server' in sys.argv:
    os.system(
        'npx tailwind build ./assets/css/styles.css -o site/assets/css/styles.css')
    run()

# Watch for changes
if 'watch' in sys.argv:
    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        paths = [
            'pages',
            'resume',
            'templates'
        ]
        for path in paths:
            event_handler = RegenerateSite()
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()

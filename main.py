'''
Highlight v 0.1.1

Featuring a completely reworked server engine.

Breaking changes:
- Remove compile command, switch to build
- Modernized TailwindCSS

Features:
- package.json scripts (requires python3 as a valid command line prompt)
- Local fonts (Github's Mona and Hubot)
- Reworked server and watch engine

CREDITS
Core server based on: https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
'''
import sys
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.build import GenerateSite
from app.server import HighlightServer
from app.watch import signal_handler
from app.helpers import watch_paths

if 'build' in sys.argv:
    # Generate site for public use.
    site = GenerateSite(compile=True)
    exit()

# Generate site for local use.
site = GenerateSite(compile=False)
print('Initial site built')

# Watchdog event handler
class WatchSiteFiles(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        site.dispatch(event)

if __name__ == '__main__':
    observer = None
    if '--watch' in sys.argv:
        # Set up Watchdog
        event_handler = WatchSiteFiles()
        observer = Observer()

        for path in watch_paths():
            observer.schedule(event_handler, path, recursive=True)
        
        observer.start()

    # Set up HTTP server
    server = HighlightServer()

    # Set up signal handling to manage server quit
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, server, observer))
    server.run()

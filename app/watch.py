import time
import logging
from watchdog.observers import Observer
from app.write import RegenerateSite, generate_site


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

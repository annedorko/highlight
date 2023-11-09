import os

# Function to handle Ctrl+C
def signal_handler(sig, frame, server=None, observer=None):
    print('Shutting down Highlight server...')
    if observer:
        print('Closing file watcher...')
        observer.stop()
        observer.join()
    if server:
        print('Closing server...')
        server.httpd().server_close()
    print('Highlight shut down.')
    os._exit(0) 

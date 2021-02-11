import urllib
import hashlib
import os
import markdown


def load_pages():
    PAGES = {}
    for page in os.listdir('pages'):
        file_path = os.path.join('pages', page)

        with open(file_path, 'r') as file:
            md = markdown.Markdown(extensions=['meta'])
            # Process HTML
            html = md.convert(file.read())
            # Process metadata, return each as string
            meta = {}
            for m in md.Meta:
                meta[m] = md.Meta[m][0]
            # Clean filename
            filename_ext = os.path.basename(file.name)
            filename = os.path.splitext(filename_ext)[0]
            # Add to overall page collection
            PAGES[page] = {
                'filename': filename,
                'content': html,
                'meta': meta,
            }
    return PAGES


def tailwind_os(status=''):
    tailwind = 'npx tailwind build ./assets/css/styles.css -o site/assets/css/styles.css'
    if status == 'compile':
        tailwind += ' -c tailwind.prod.config.js'
    return tailwind


def set_gravatar(email, default, size):
    encoded_email = email.encode('utf-8')
    hashed_email = hashlib.md5(encoded_email.lower()).hexdigest()
    gravatar_url = "https://www.gravatar.com/avatar/"
    gravatar_url += hashed_email + "?"
    gravatar_url += urllib.parse.urlencode(
        {
            'd': default,
            's': str(size)
        })
    return gravatar_url

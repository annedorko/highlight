import urllib
import hashlib


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

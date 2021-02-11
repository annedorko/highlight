import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from app.helpers import set_gravatar, load_pages


def get_global(compile=False):
    # Get person information
    with open('resume/about.yaml', 'r') as about_file:
        about = load(about_file, Loader=Loader)
    # Get Gravatar image
    about['gravatar'] = set_gravatar(
        about['email'],
        'assets/media/avatar.jpg',
        40)
    # Get global site settings
    with open('config.yaml', 'r') as config:
        settings = load(config, Loader=Loader)
    settings['cname'] = settings['url']
    if compile == False:
        settings['url'] = 'http://localhost:4242'
    # Get pages for navigation
    NAV = {}
    PAGES = load_pages()
    for page in PAGES:
        p = PAGES[page]
        # TODO: Optional page exclusion
        title = p['meta'].get('title')
        if 'anchor' in p['meta']:
            title = p['meta'].get('anchor')
        NAV[p['filename']] = {
            'href': settings['url'] + '/' + p['filename'] + '.html',
            'anchor': title
        }
    settings['nav'] = NAV
    site = {
        "site": settings,
        "person": about
    }
    return site

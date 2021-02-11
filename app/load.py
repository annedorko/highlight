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
        about['contact']['email'],
        'assets/media/avatar.jpg',
        40)
    # Clean links
    if 'links' in about:
        links = {}
        all_links = about['links']
        for link in all_links:
            fresh_link = {}
            if not type(all_links[link]) is dict:
                fresh_link = {
                    'url': all_links[link],
                    'text': all_links[link],
                    'icon': '<i class="fas fa-globe"></i>'
                }
            else:
                fresh_link = all_links[link]
                if not 'text' in fresh_link:
                    fresh_link['text'] = fresh_link['url']
                if not 'icon' in fresh_link:
                    fresh_link['icon'] = '<i class="fas fa-globe"></i>'
            links[fresh_link['url']] = fresh_link
        about['links'] = links
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
            'href': settings['url'] + '/' + p['filename'],
            'anchor': title
        }
    settings['nav'] = NAV
    site = {
        "site": settings,
        "person": about
    }
    return site

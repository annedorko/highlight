from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from app.helpers import set_gravatar, set_github_avatar, load_pages, load_roles

def get_global(compile=False):
    # Get global site settings
    with open('src/config.yaml', 'r') as config:
        settings = load(config, Loader=Loader)
    settings['cname'] = settings['url']
    if compile == False:
        settings['url'] = 'http://localhost:4242'
    # Get person information
    with open('src/resume/about.yaml', 'r') as about_file:
        about = load(about_file, Loader=Loader)
    # Get Gravatar image
    if settings['avatar'] and 'github' == settings['avatar'] and about['contact']['github']:
        about['avatar'] = set_github_avatar(
            about['contact']['github'],
            250
        )
    else:
        about['avatar'] = set_gravatar(
            about['contact']['email'],
            'src/assets/media/avatar.jpg',
            250)
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
    # Get pages for navigation
    NAV = {}
    PAGES = load_pages()
    SET_PAGES = {}
    for page in PAGES:
        p = PAGES[page]
        # TODO: Optional page exclusion
        title = p['meta'].get('title')
        if 'anchor' in p['meta']:
            title = p['meta'].get('anchor')
        SET_PAGES[p['filename']] = {
            'href': settings['url'] + '/' + p['filename'],
            'anchor': title,
            'order': p['meta'].get('order') if 'order' in p['meta'] else 2,
        }
    sort_pages = sorted(
        SET_PAGES.items(), key=lambda x: x[1]['order'])
    for i, p in sort_pages:
        NAV[i] = p
    settings['nav'] = NAV
    # Get roles
    settings['roles'] = load_roles()
    site = {
        "site": settings,
        "person": about,
    }
    return site

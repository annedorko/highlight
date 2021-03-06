import os
import shutil
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from app.server import run
from app.load import get_global
from app.helpers import load_pages, load_history


class RegenerateSite(LoggingEventHandler):

    def dispatch(self, event):
        site = get_global()
        generate_site(site, False)
        print('Site regenerated: ', event)


def remove_old_site():
    print('Removing old site')
    for root, dirs, files in os.walk('site/'):
        delete = ['.html', 'CNAME', '.nojekyll', 'css', 'assets']
        for f in files:
            file = os.path.join(root, f)
            if any(search in file for search in delete):
                os.unlink(file)
        for d in dirs:
            dir = os.path.join(root, d)
            if any(search in dir for search in delete):
                shutil.rmtree(dir)


def write_base_files(url):
    # .nojekyll for GitHub Pages
    with open('site/.nojekyll', 'w') as file:
        file.write('')
    # CNAME for GitHub Pages custom subdomain
    with open('site/CNAME', 'w') as file:
        file.write(url)


def generate_homepage(env, site):
    meta = {
        'title': site['person']['name']
    }
    # Set template
    template = env.get_template('home.html')
    # Write page to template
    page = template.render(
        meta=meta,
        person=site['person'],
        site=site['site'],
    )
    # Save page
    with open('site/index.html', 'w') as file:
        file.write(page)


def generate_pages(env, site, single=False):
    PAGES = load_pages()

    for p in PAGES:
        slug = PAGES[p].get('filename')
        content = PAGES[p].get('content')
        meta = PAGES[p].get('meta')
        # Set template
        set_template = 'page'
        if 'template' in meta:
            set_template = meta.get('template')
        template = env.get_template(set_template + '.html')
        # Write page to template
        page = template.render(
            page=content,
            meta=meta,
            person=site['person'],
            site=site['site']
        )
        # Set slug
        if 'slug' in meta:
            slug = meta.slug
        # Save page
        with open('site/' + slug + '.html', 'w') as file:
            file.write(page)


def generate_resume(env, site):
    ROLES = site.get('site').get('roles')
    RESUMES = {}
    for role in ROLES:
        r = ROLES[role]
        # Get related history items
        history = load_history(r['role'])
        # Set meta
        meta = {
            'title': r.get('role')
        }
        # Set slug
        slug = r.get('slug')
        if 'slug' in meta:
            slug = meta.slug
        # Set template
        set_template = 'resume'
        if 'template' in meta:
            set_template = meta.get('template')
        template = env.get_template(set_template + '.html')
        # Write page to template
        page = template.render(
            meta=meta,
            role=r,
            person=site['person'],
            site=site['site'],
            experience=history
        )
        # Save page
        with open('site/' + slug + '.html', 'w') as file:
            file.write(page)


def generate_site(site, delete=True):
    env = Environment(loader=FileSystemLoader('templates'))
    if delete == True:
        remove_old_site()
        write_base_files(site['site'].get('cname'))
    generate_homepage(env, site)
    generate_pages(env, site)
    generate_resume(env, site)

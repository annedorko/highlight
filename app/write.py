import os
import markdown
from jinja2 import Environment, FileSystemLoader
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from app.server import run
from app.load import get_global


class RegenerateSite(LoggingEventHandler):

    def dispatch(self, event):
        site = get_global()
        generate_site(site)
        print('Site regenerated: ', event)


def generate_site(site):
    env = Environment(loader=FileSystemLoader('templates'))
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
            person=site['person']
        )
        # Set slug
        if 'slug' in meta:
            slug = meta.slug
        # Save page
        with open('site/' + slug + '.html', 'w') as file:
            file.write(page)

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
    # Convert contents to Markdown
    with open('pages/page.md', 'r') as file:
        # Meta returns as a Dictionary with lists
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(file.read())

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('wrapper.html')

        data = {
            'content': html,
            'title': md.Meta.get('title')[0]
        }
        page = template.render(post=data, person=site['person'])
        with open('site/index.html', 'w') as file:
            file.write(page)

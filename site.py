# Tutorial
# https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
import os
import sys
import markdown
from jinja2 import Environment, FileSystemLoader
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Get global site settings
with open('resume/about.yaml', 'r') as about_file:
    about = load(about_file, Loader=Loader)

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
    page = template.render(post=data, person=about)
    with open('site/index.html', 'w') as file:
        file.write(page)

# Render CSS
os.system(
    'npx tailwindcss-cli@latest build ./assets/css/styles.css -o site/assets/css/styles.css')

# Optionally run localhost server
if 'server' in sys.argv:
    os.system('python -m http.server 4242 -d site/')

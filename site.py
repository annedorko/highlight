# Tutorial
# https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
import os
import sys
import markdown
from jinja2 import Environment, FileSystemLoader

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
    page = template.render(post=data)
    with open('site/index.html', 'w') as file:
        file.write(page)

# Render CSS
os.system(
    'npx tailwindcss-cli@latest build ./assets/css/styles.css -o site/assets/css/tailwind.css')

# Optionally run localhost server
if 'server' in sys.argv:
    os.system('python -m http.server 4242 -d site/')

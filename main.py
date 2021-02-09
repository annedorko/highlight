# Tutorial
# https://blog.naveeraashraf.com/posts/make-static-site-generator-with-python-2/
import markdown
from jinja2 import Environment, PackageLoader

# Convert contents to Markdown
with open('content/page.md', 'r') as file:
    # Meta returns as a Dictionary with lists
    md = markdown.Markdown(extensions=['meta'])
    html = md.convert(file.read())

    env = Environment(loader=PackageLoader('main', 'templates'))
    template = env.get_template('wrapper.html')

    data = {
        'content': html,
        'title': md.Meta.get('title')[0],
        'date': md.Meta.get('date')[0]
    }

    page = template.render(post=data)
    with open('site/index.html', 'w') as file:
        file.write(page)

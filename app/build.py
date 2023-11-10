import os
import shutil
from jinja2 import Environment, FileSystemLoader
from app.load import get_global
from app.helpers import load_pages, load_history

class GenerateSite():
    def __init__(self, compile=False):
        self.data = {
            'compile': compile,
            'has_compiled': False,
            'site': get_global(compile=compile),
            'env': Environment(loader=FileSystemLoader('src/templates'))
        }
        print('Generating the site...')
        self.build()

    def dispatch(self, event):
        print('Site regenerating on changed file:', event.src_path, '')
        self.build(regenerate=True)
        print('Site regenerated.')

    def build(self, destroy=False, regenerate=False):
        if regenerate:
            self.data['compile'] == False
        # Build site directory if it does not exist.
        if not os.path.exists('site'):
            os.mkdir('site')
        # Clear old site files.
        if self.data['compile'] or destroy:
            self.destroy()
            self.write_base_files()
        # Generate new site files.
        self.data['site'] = get_global(compile=self.data['compile'])
        self.generate_homepage()
        self.generate_pages()
        self.generate_resume()
        if regenerate or not self.data['has_compiled']:
            self.generate_assets()
        self.data['has_compiled'] = True
        return
    
    def generate_assets(self):
        postcss = 'npx postcss ./src/assets/css/styles.css -o ./site/assets/css/styles.css'
        os.system(postcss)

    def destroy(self):
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

    def write_base_files(self):
        url = self.data['site']['site'].get('cname')
        # .nojekyll for GitHub Pages
        with open('site/.nojekyll', 'w') as file:
            file.write('')
        # CNAME for GitHub Pages custom subdomain
        with open('site/CNAME', 'w') as file:
            file.write(url)
        # Copy in local fonts.
        source_fonts = 'src/assets/fonts'
        destination_fonts = 'site/assets/fonts'
        shutil.copytree(source_fonts, destination_fonts, dirs_exist_ok=True)
    
    def generate_homepage(self):
        env = self.data['env']
        site = self.data['site']

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


    def generate_pages(self, single=False):
        env = self.data['env']
        site = self.data['site']
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

    def generate_resume(self):
        env = self.data['env']
        site = self.data['site']

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


import urllib
import hashlib
import os
import markdown
import yaml
import datetime
import math
from slugify import slugify

def watch_paths():
    paths = [
        'src/pages',
        'src/resume',
        'src/templates',
        'src/assets/css',
    ]
    return paths

def load_history(role):
    PAST = {}
    CURRENT = {}
    # Set file names
    LIST = {}
    for page in os.listdir('src/resume/history'):
        LIST[page] = os.path.join('src/resume/history', page)
    # Read YAML from each file
    for item in LIST:
        # Load experience
        experience = False
        with open(LIST[item], 'r') as stream:
            try:
                experience = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        # Process experience
        include = False
        if not experience is False:
            # Optionally allow job: definition
            if experience.get('job'):
                experience = experience.get('job')
            # Is this listed as included?
            includes = experience.get('include')
            look_for = ['All', role]
            if includes and any(search in includes for search in look_for):
                include = True
            # Is this role explicitly excluded for this experience?
            excludes = experience.get('exclude')
            if excludes and any(search in excludes for search in [role]):
                include = False
        # If including, carry on
        if include is True:
            # Process YAML data to pass onto page
            # titles (default, Role)
            # company
            # location
            # url
            # type
            # dates (YYYY-MM): start, end
            # skills: base, default, Role
            # descriptions: default, Role
            title = experience.get('titles')[role] if role in experience.get(
                'titles') else experience.get('titles')['default']
            # print('MATH FOR JOB TITLE', title)
            base_skills = experience.get('skills')['base']
            special_skills = experience.get('skills')[role] if role in experience.get(
                'skills') else experience.get('skills')['default']
            skills = base_skills + special_skills
            description = experience.get('descriptions')[role] if role in experience.get(
                'descriptions') else experience.get('descriptions')['default']
            start = ''
            end = 'Present'
            sort = datetime.datetime.now()
            if 'dates' in experience:
                if 'start' in experience.get('dates'):
                    start_dt = experience.get('dates')['start']
                    start_dt_obj = datetime.datetime.strptime(
                        start_dt, '%Y-%m')
                    start_formatted = datetime.datetime.strftime(
                        start_dt_obj, '%b %Y')
                    start = start_formatted
                if 'end' in experience.get('dates') and not experience.get('dates')['end'] == 'Present':
                    end_dt = experience.get('dates')['end']
                    end_dt_obj = datetime.datetime.strptime(
                        end_dt, '%Y-%m')
                    end_formatted = datetime.datetime.strftime(
                        end_dt_obj, '%b %Y')
                    end = end_formatted
                    sort = start_dt_obj
                    length = date_diff(start_dt_obj, end_dt_obj)
                else:
                    sort = start_dt_obj + datetime.timedelta(days=2)
                    length = date_diff(
                        start_dt_obj, datetime.datetime.now())

            bundle = {
                'role': title,
                'company': experience.get('company') if 'company' in experience else '',
                'location': experience.get('location') if 'location' in experience else '',
                'url': experience.get('url') if 'url' in experience else '',
                'type': experience.get('type') if 'type' in experience else '',
                'skills': skills,
                'description': description,
                'sort': sort,
                'start': start,
                'end': end,
                'length': length
            }
            if bundle['end'] == 'Present':
                CURRENT[item] = bundle
            else:
                PAST[item] = bundle
                # End inclusion if statement
                # TODO sort relavent history by date
    WORK = {}
    sort_past = sorted(
        PAST.items(), key=lambda x: x[1]['sort'], reverse=True)
    sort_current = sorted(
        CURRENT.items(), key=lambda x: x[1]['sort'], reverse=True)
    for i, h in sort_current:
        WORK[i] = h
    for i, h in sort_past:
        WORK[i] = h
    return WORK


def load_roles():
    ROLES = {}
    with open("src/resume/roles.yaml", 'r') as stream:
        try:
            find = yaml.safe_load(stream)
            # Turn list into dictionary
            for f in find:
                ROLES[f['role']] = f
                if not 'slug' in ROLES[f['role']]:
                    ROLES[f['role']]['slug'] = slugify(f['role'])
        except yaml.YAMLError as exc:
            print('error')
    return ROLES


def load_pages():
    PAGES = {}
    for page in os.listdir('src/pages'):
        file_path = os.path.join('src/pages', page)

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
    return PAGES


def tailwind_os(status=''):
    postcss = 'npx postcss ./assets/css/styles.css -o ./site/assets/css/styles.css'
    return postcss

def set_github_avatar(github, size):
    github_url = 'https://github.com/'
    github_url += github
    github_url += '.png?size=' + str(size)
    return github_url

def set_gravatar(email, default, size):
    encoded_email = email.encode('utf-8')
    hashed_email = hashlib.md5(encoded_email.lower()).hexdigest()
    gravatar_url = "https://www.gravatar.com/avatar/"
    gravatar_url += hashed_email + "?"
    gravatar_url += urllib.parse.urlencode(
        {
            'd': default,
            's': str(size)
        })
    return gravatar_url

def date_diff(then, now, format='%Y-%m'):
    # Ensure we are working with datetime values.
    now = now if isinstance(now, datetime.datetime) else datetime.datetime.strptime(now, format)
    then = then if isinstance(then, datetime.datetime) else datetime.datetime.strptime(then, format)
    # Calculate the difference between the dates.
    diff = now - then
    # Extract years and remaining days.
    years = diff.days // 365
    remaining_days = diff.days % 365
    # Convert remaining days to months.
    months = math.ceil(remaining_days / 30) if remaining_days > 14 else remaining_days // 30
    # Avoid accidentally rounding up to 12 months or more.
    if months > 11:
        years += 1
        months -= 12
    # Convert date dato to human readable string.
    date_info = []
    if years > 0:
        date_info.append(f"{years} {'yr' if years == 1 else 'yrs'}")
    if months > 0:
        date_info.append(f"{months} {'mo' if months == 1 else 'mos'}")
    return " ".join(date_info)
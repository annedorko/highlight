import urllib
import hashlib
import os
import markdown
import yaml
import datetime
import math
from slugify import slugify
from operator import itemgetter


def date_diff(older, newer):
    """
    Returns a humanized string representing time difference

    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns '4 days'
    0 days 4 hours 3 minutes returns '4 hours', etc...
    """

    # Min-max month estimates
    # Oldest month starts on the 1st
    # Newest month starts on the 28th
    timeDiff = newer.replace(day=28) - older.replace(day=1)
    days = timeDiff.days
    hours = timeDiff.seconds / 3600
    minutes = timeDiff.seconds % 3600 / 60
    seconds = timeDiff.seconds % 3600 % 60
    months = timeDiff.days / 30
    years = timeDiff.days / 365

    str = ""
    tStr = ""
    if years > 1:
        # Check years
        if years == 1:
            tStr = "yr"
        else:
            tStr = "yrs"
        str = str + "%s %s" % (math.floor(years), tStr)
        months = months - (math.floor(years) * 12)
        if months > 1:
            if months == 1:
                tStr = "mo"
            else:
                tStr = "mos"
            str += " %s %s" % (math.ceil(months), tStr)
        return str
    elif months > 1:
        if months == 1:
            tStr = "mo"
        else:
            tStr = "mos"
        str = str + "%s %s" % (round(months), tStr)
        return str
    elif days > 0:
        if days == 1:
            tStr = "day"
        else:
            tStr = "days"
        str = str + "%s %s" % (days, tStr)
        return str
    elif hours > 0:
        if hours == 1:
            tStr = "hour"
        else:
            tStr = "hours"
        str = str + "%s %s" % (hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:
            tStr = "min"
        else:
            tStr = "mins"
        str = str + "%s %s" % (minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:
            tStr = "sec"
        else:
            tStr = "secs"
        str = str + "%s %s" % (seconds, tStr)
        return str
    else:
        return None


def load_history(role):
    PAST = {}
    CURRENT = {}
    # Set file names
    LIST = {}
    for page in os.listdir('resume/history'):
        LIST[page] = os.path.join('resume/history', page)
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
            includes = experience.get('include')[0]
            look_for = ['All', role]
            if any(search in includes for search in look_for):
                include = True
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
        CURRENT.items(), key=lambda x: x[1]['sort'])
    for i, h in sort_current:
        WORK[i] = h
    for i, h in sort_past:
        WORK[i] = h
    return WORK


def load_roles():
    ROLES = {}
    with open("resume/roles.yaml", 'r') as stream:
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
    return PAGES


def tailwind_os(status=''):
    tailwind = 'npx tailwind build ./assets/css/styles.css -o site/assets/css/styles.css'
    if status == 'compile':
        tailwind += ' -c tailwind.prod.config.js'
    return tailwind


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

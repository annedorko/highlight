import urllib
import hashlib
import os
import markdown
import yaml
import datetime
import math


def date_diff(older, newer):
    """
    Returns a humanized string representing time difference

    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns '4 days'
    0 days 4 hours 3 minutes returns '4 hours', etc...
    """

    timeDiff = newer - older
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
    HISTORY = {}
    for page in os.listdir('resume/history'):
        file_path = os.path.join('resume/history', page)
        with open(file_path, 'r') as stream:
            try:
                exp = yaml.safe_load(stream)
                includes = exp.get('include')[0]
                look_for = ['All', role]
                # Turn list into dictionary
                if any(search in includes for search in look_for):
                    # Process YAML data to pass onto page
                    # titles (default, Role)
                    # company
                    # location
                    # url
                    # type
                    # dates (YYYY-MM): start, end
                    # skills: base, default, Role
                    # descriptions: default, Role
                    title = exp.get('titles')[role] if role in exp.get(
                        'titles') else exp.get('titles')['default']
                    base_skills = exp.get('skills')['base']
                    special_skills = exp.get('skills')[role] if role in exp.get(
                        'skills') else exp.get('skills')['default']
                    skills = base_skills + special_skills
                    description = exp.get('descriptions')[role] if role in exp.get(
                        'descriptions') else exp.get('descriptions')['default']
                    # TODO: start dates at first of month, end dates at last day of month
                    start = ''
                    end = 'Present'
                    if 'dates' in exp:
                        if 'start' in exp.get('dates'):
                            start_dt = exp.get('dates')['start']
                            start_dt_obj = datetime.datetime.strptime(
                                start_dt, '%Y-%m')
                            start_formatted = datetime.datetime.strftime(
                                start_dt_obj, '%b %Y')
                            start = start_formatted
                        if 'end' in exp.get('dates') and not exp.get('dates')['end'] == 'Present':
                            end_dt = exp.get('dates')['end']
                            end_dt_obj = datetime.datetime.strptime(
                                end_dt, '%Y-%m')
                            end_formatted = datetime.datetime.strftime(
                                end_dt_obj, '%b %Y')
                            end = end_formatted
                            length = date_diff(start_dt_obj, end_dt_obj)
                        else:
                            length = date_diff(start_dt_obj, datetime.now())

                    HISTORY[page] = {
                        'role': title,
                        'company': exp.get('company') if 'company' in exp else '',
                        'location': exp.get('location') if 'location' in exp else '',
                        'url': exp.get('url') if 'url' in exp else '',
                        'type': exp.get('type') if 'type' in exp else '',
                        'skills': skills,
                        'description': description,
                        'start': start,
                        'end': end,
                        'length': length
                    }
                    # End if any
            except yaml.YAMLError as exc:
                return
    # TODO sort relavent history by date
    return HISTORY


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

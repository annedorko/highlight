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

def date_diff(then, now):
    # Measure length of time spent at a job or on a project in years, months
    # NOTE: The following methods look a little convoluted, as uneven months, leap years, etc. made long-term contract terms clearly incorrect

    # Set up standard datetime diff to work with
    standard_diff = now - then
    # Do math using years (i.e. 2020, 2019) if there is more than 365 days difference on the standard diff
    years = now.year - then.year if standard_diff.days > 365 else 0
    # If more than 1 year of time and the months aren't the same (i.e. Mar-Mar, Apr-Apr), crunch the difference in months
    if years > 0 and then.month != now.month:
        # Calculate months per year on the job, starting at 0
        months = 0
        # Add 1 to range end since range is exclusive of the final value
        for i in range(then.year, now.year + 1):
            if i == then.year:
                # How many months of experience in the first year? December = 1 (i.e. 13-12=1), January = 12 (i.e. 13-1=12)
                months += 13 - then.month
                # print('months for', i, ':', (13 - then.month))
            elif i == now.year:
                # The number month works plainly
                months += now.month
            else:
                # Each non starting and non ending year gets accounted for 12 months
                months += 12
        year_in_months = years * 12
        # If we have fewer months than the number of months in the total years worked, we need to subtract a year and try again (this accounts for dates where the start/end months don't allow for full year calculations between years i.e. Starting in Dec 2018 and ending in Jan 2021 is not 3 years of experience since only one month is worked in both 2018 and 2021. The result is 2 years (2019, 2020) plus the two months)
        if months < year_in_months:
            years -= 1
            year_in_months = years * 12
        months = months - (years * 12)
    elif then.month == now.month:
        # Months match so the difference in months is zero
        months = 0
    else:
        # If less than one year, it is accurate enough to divide by 30
        # Always round up to match LinkedIn
        month_diff = math.ceil(standard_diff.days / 30)
        months = month_diff if month_diff < 12 else 11
    str = ""
    tStr = ""
    if years > 1:
        # Check years
        if years == 1:
            tStr = "yr"
        else:
            tStr = "yrs"
        str = str + "%s %s" % (math.floor(years), tStr)
        if months > 1:
            # print('MONTHS IS ', months)
            if months == 1:
                tStr = "mo"
            else:
                tStr = "mos"
            str += " %s %s" % (months, tStr)
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
    else:
        return None
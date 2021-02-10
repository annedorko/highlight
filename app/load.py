from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from app.helpers import set_gravatar


def get_global():
    # Get global site settings
    with open('resume/about.yaml', 'r') as about_file:
        about = load(about_file, Loader=Loader)
    # Get Gravatar image
    about['gravatar'] = set_gravatar(
        about['email'],
        'assets/media/avatar.jpg',
        40)
    site = {
        "person": about
    }
    return site

# Highlight: a Static Site Generator

Highlight is a lightweight, opinionated Static Site Generator (SSG) for quickly creating a beautiful resume and portfolio site that targets multiple ideal roles.

**Note:** This project is experimental. Use at your own risk!

## Who is it for?

Highlight is built by and for generalists, who often need tweaked versions of their resume and portfolio to be appealing for different opportunities. This SSG is built to help you _highlight_ the right parts of your diverse skillset and experiences to the right people, quickly and elegantly.

Because the output is a static site, you can host your resume and portfolio from nearly anywhere. Free static site hosting is available with [GitHub Pages](https://pages.github.com/). View the demo portfolio hosted at [GitHub Pages here](https://hire.annedorko.com).

## Built With

- [TailwindCSS](https://github.com/tailwindlabs/tailwindcss)

## Getting Started

If you use this project base, modify this project to suit your own resume and portfolio activities!

### Prerequisites

Built using:

- Python 3
- Node.js 15+
- NPM 7+

The program may work on lower versions of Node or NPM.

### Installation

1. Clone this repo into a clean project folder.
2. Install NPM packages using `npm install`
3. Generate the site in the console using `python site.py`
4. Static site is now available for local browsing in `site/`

## Usage

This repo is full of example data. Currently, that data is my own resume information. You will want to use this as a reference to create your own site.

Data in Highlights is managed through [YAML](https://yaml.org/refcard.html). If you receive errors it is likely because the YAML got mis-formatted. Be sure to follow the same indentations and patterns as provided in the example data!

### Step 1. Configure Site

1. Open `config.yaml`
2. Change the `url` setting to the root domain your site will be published at.

This URL controls:
- The root of your links throughout the site
- The CNAME for Github Pages to support custom domains

_Note: Highlights automatically generates a .nojekyll file for Github Pages, as well._

### Step 2. Start Site for Local Editing

Open two console tabs and navigate to the project root in both.

**First,** run `python site.py server` and navigate to [http://localhost:4242](http://localhost:4242) to preview your site live.

**Next,** run `python site.py watch` in the other tab to regenerate the site automatically as you make changes to `/pages`, `/resume`, and `/templates` in the following steps.

### Step 3. Update Your Bio

1. Open `resume/about.yaml`
2. Edit the values to reflect your name, contact information, skills, and more.

This document is for the data that is the same across all your resume and portfolio items.

- Name
- Tagline
- Work availability
- Skills grouped by category
- Important links
- Contact information
- Education

#### Skills

Categories can be written using alphanumeric values followed by a colon. If you need to include a colon in your category name, be sure to surround it with quotes.

For example:

- Good: `Music Production:`
- Good: `'Music: Production':`
- Bad: `Music: Production:`

#### Links

Links can be plain text, like so:

`Homepage: 'https://www.annedorko.com'`

Or, you can optionally provide a URL, anchor text, and even a [FontAwesome icon](https://fontawesome.com/icons?d=gallery&m=free). This makes your resume look much cleaner and enables you to include icons for Twitter, LinkedIn, or whatever sites you may be referencing.

_Without icon:_
```
Homepage:
  url: 'https://www.annedorko.com'
  text: 'annedorko.com'
```

_With icon:_
```
Homepage:
  url: 'https://www.annedorko.com'
  text: 'annedorko.com'
  icon: '<i class="fas fa-home"></i>'
```

#### about.yaml Template

Here is a blank template with a few required stand-ins if you’d like to start from scratch. Feel free to cross-reference these values with the default about.yaml to better understand how to use them.

```
---
  name: ''
  taglines:
    default: ''
  open:
    available: true
    seeking: ''
    location: ''
  skills:
    Your Category Here:
      - skill: Write a Skill
        years: 1
      - skill: Another Skill
        years: 4
    Your 2nd Category Here:
      - skill: Another Skill
        years: 2
  links:
    Homepage:
      url: ''
      text: ''
    LinkedIn: 'https://linkedin.com'
  contact:
    email: ''
    phone: ''
    timezone: ''
  education:
    Degree Name Here:
      school: ''
      degree: ''
      study: ''
      graduation: ''
```

### Step 4. Add Your Target Roles

Modify target roles and professional summaries using `resume/roles.yaml`

### Step 5. Add Your Work History

Modify career history under `resume/history/`

### Step 6. Edit, Add, and Delete Site Pages

Your site pages are managed in markdown files under `pages/`

### Step 7. Compile Your Website for Uploading

Once you are satisfied with your site, use CTRL+C in the console to stop watching for changes in your site and close the server.

Run `python site.py compile` to compile the site using Tailwind CSS at production size. Once compiled, upload the contents of `site/` to your host of choice! I recommend free GitHub Pages.

## Roadmap

See [open issues](https://github.com/annedorko/highlight/issues) for a list of proposed features and known issues.

## License

Distributed under the `GNU GPLv3` license. See `LICENSE` for more information.

## Contact

Anne Dorko - [LinkedIn](https://www.linkedin.com/in/annedorko) - [@annedorko](https://twitter.com/annedorko) - [anne@dorko.tv](mailto:anne@dorko.tv)

Project Link: [github.com/annedorko/highlight](https://github.com/annedorko/highlight)

## Acknowledgements

This project was to get my own flexible resume and portfolio running as well as experiment with Python in a new environment. Below are packages I used and resources I referenced along the way.

### Packages
- [Python-Markdown](https://github.com/Python-Markdown/markdown)
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
- [watchdog](https://pypi.org/project/watchdog/)
- [unicode_slugify](https://pypi.org/project/unicode-slugify/)

### Resources
- [othneildrew’s Best README Template](https://github.com/othneildrew/Best-README-Template)
- [nqcm’s Static Site Generator Tutorial](https://github.com/nqcm/static-site-generator)
- [Ansible YAML Syntax Documentation](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)

<h1 align="center">Highlight: a Static Site Generator</h1>

<p align="center">Highlight is a lightweight, opinionated Static Site Generator (SSG) for quickly creating a beautiful resume and portfolio site that targets multiple ideal roles.</p>

![Highlight Site Preview](https://user-images.githubusercontent.com/1281008/107776426-d93eb780-6d41-11eb-85b9-c3954b4fe843.png)

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

- Python 3 (Required)
- Node.js 15+
- NPM 7+

The program may work on lower versions of Node or NPM.

### Installation

1. Clone this repo into a clean project folder.
  ```
  git clone https://github.com/annedorko/highlight.git
  ```
2. Navigate into your project folder using the console.
3. Install NPM packages
  ```
  npm install
  ```
4. Install Python requirements
  ```shell
  pip install -r requirements.txt  
  ```
  ...or...
  ```shell
  pipenv install  
  ```
  ...or...
  ```shell
  conda install --file requirements.txt
  ```
5. Generate the site in the console.
  ```
  python site.py
  ```
6. Static site files are now available for local browsing in `site/`

## Usage

This repo is full of example data. Currently, that data is my own resume information. You will want to use this as a reference to create your own site.

Data in Highlight is managed through [YAML](https://yaml.org/refcard.html). If you receive errors it is likely because the YAML got mis-formatted. Be sure to follow the same indentations and patterns as provided in the example data!

### Step 1. Configure Site

1. Open `config.yaml`
2. Change the `url` setting to the root domain your site will be published at.

This URL controls:
- The root of your links throughout the site
- The CNAME for Github Pages to support custom domains

_Note: Highlight automatically generates a .nojekyll file for Github Pages, as well._

### Step 2. Start Site for Local Editing

Open two console tabs and navigate to the project root in both.

**First,** run `python site.py server`. You can now navigate to [http://localhost:4242](http://localhost:4242) in your browser to preview your site live.

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

Your email will also be used to pull your Gravatar image, so I recommend ensuring you have an account there associated with your work email. Set up a professional photo that looks great on the homepage.

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

1. Open `resume/roles.yaml`
2. Edit the values to reflect your target roles.

This document is the root of all your generated resumes. There is no limit to the number of target roles you can add, as long as you follow the YAML format! **Every role you add will generate a new resume page targeted towards that role.**

Every role requires:

- Role/Title Name
- Professional Summary
- List of Essential Skills (Multiples of 3 work best)

#### Preview Role Summary
<p align="center"><img style="max-width: 250px; height: auto;" src="https://user-images.githubusercontent.com/1281008/107766163-5ca4dc80-6d33-11eb-9448-33310821f2f0.png" width="600" /></p>

This information will appear at the top of your resume, as shown above.

#### role.yaml Template

Here is a blank template with a few required stand-ins if you’d like to start from scratch. Feel free to cross-reference these values with the default role.yaml to better understand how to use them.

```
---
  - role: Role Name
    summary: Professional summary.
    skills:
      - Skill 1
      - Skill 2
      - Skill 3
  - role: 2nd Role Name
    summary: Professional summary.
    skills:
      - Skill 1
      - Skill 2
      - Skill 3
```

### Step 5. Add Your Work History

Without adding any career history, your generated resumes will look a bit empty. You will need to add work history to your `resume/history/` folder.

Each file represents a single element that will show up on your resumes. You will need to add a new file per work history item.

The file names don’t matter, so long as they are unique. I use a `YYYY-company-name.yaml` format so it’s easier to find what I’m looking for later.

These documents define:

- Which resumes to include the experience on.
- The role you played, adjustable per target resume role.
- Company name
- Company location
- Company URL
- Type of work (Full-time, part-time, freelance, etc.)
- Dates: Start and end. Requires a 'YYYY-MM' format for both values, or you can use 'Present' for end date.
- Skills used on the job. Base is for all target roles, default is used by default, or you can add target-role-specific lists as well. Will be relevant on portfolio pages in the future.
- Description, adjustable per target resume role.

Titles and descriptions all both required, and both require default values.

Skills are not required. If included, skills require both base and default values. (Currently, skills are not necessary to add here but will be helpful for when portfolio pages are available in the app.)

If you do not follow the required date format, the script will not run correctly. The script will automatically supply the number of years and months.

#### Adding and Customizing Work Experience to a Target Role Resume

To add a work experience to all resumes, use:
```
include:
  - All
```

To add a work experience to specific resumes, list them under include in a list.

```
include:
  - Target Role
  - Target Role 2
  - Target Role 3
```

Titles and descriptions need a default title, to start. If you would like to change your title role for specific resumes, you can do so by listing the name of the target role followed by the name of your changed title.

This is particularly helpful if you played many roles within a company, and want to highlight one role over another for a specific resume.

```
titles:
  default: Job Title
  Target Role: Adjusted Job Title
  Target Role 3: Secondary Job Title
```

In the above example, "Job Title" will show by default on any resume you include it on. Resumes for "Target Role" and "Target Role 3" will be customized to use the provided titles.

The same goes for descriptions!

```
descriptions:
  default: Job Title
  Target Role 2: Adjusted Job Title
```

You can add as many or few customizations as necessary. The default will always be used if you have not provided a specific version. I recommend starting with just the default, and adding customizations as needed when you generate new resumes.

#### history/*.yaml Template

Here is a blank template with a few required stand-ins if you’d like to start from scratch. Feel free to cross-reference these values with the example history files to better understand how to use them.

```
---
  include:
    - All
  titles:
    default: Job Title
  company: Company Name
  location: Company City, Country
  url: https://www.example.com/
  type: ''
  dates:
    start: 2010-03
    end: Present
  skills:
    base:
      - Skills
    default:
      - Other Skills
  descriptions:
    default: Default description of experience.
```

### Step 6. Edit, Add, and Delete Site Pages

Finally, you will need to adjust your site pages! You can add as many or few pages as you’d like. These will be linked to at the top of your site in the navigation bar. These will be useful if you plan to send the web versions of your resumes to people.

Your site pages are managed in markdown files under `pages/`. Here is an [introduction to markdown](https://www.markdownguide.org/getting-started/) if you are not familiar with it.

Since your homepage is generated automatically based on the `about.yaml` and `roles.yaml` files, do not create an `index.md` page. Otherwise, you can create whatever pages you like.

I have included a simple About and Contact page.

You can customize the order the pages show up in your navigation by changing the order value in the meta data. Lower numbers will show first, higher numbers will show later. In the example pages you can see that the About page shows first, with an order of `0`, and the contact page shows second, with an order of `2`.

You can set `title`, `slug`, and `order` in the markdown metadata.

### Step 7. Compile Your Website for Uploading

If you are running the server and watch commands, you will have been able to refresh your website to see how it changes while you adjust your data.

Once you are satisfied with your site, use CTRL+C in the console to stop watching for changes in your site and close the server.

Run `python site.py compile` to compile the site using Tailwind CSS at production size. Once compiled, upload the contents of `site/` to your host of choice! I recommend free GitHub Pages.

### Step 8: Print to PDF Using Chrome

If you need PDF versions of your resume, as I do, there are special print CSS styles. Navigate to your desired resume page and _Print to PDF_. I recommend using Chrome if you experience any formatting issues.

You can adjust the font families in `styles.css` if you are not happy with the defaults.

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

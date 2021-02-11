# Highlight: a Static Site Generator

Highlight is a lightweight, opinionated Static Site Generator (SSG) for quickly creating a beautiful resume and portfolio site that targets multiple ideal roles.

**Note:** This project is in progress and is not considered functional until [Version 1.0](https://github.com/annedorko/highlight/milestone/1) has been reached.

## Who is it for?

Highlight is built by and for generalists, who often need tweaked versions of their resume and portfolio to be appealing for different opportunities. This SSG is built to help you _highlight_ the right parts of your diverse skillset and experiences to the right people, quickly and elegantly.

Because the output is a static site, you can host your resume and portfolio from nearly anywhere. Free static site hosting is available with [GitHub Pages](https://pages.github.com/). View the demo portfolio hosted at [GitHub Pages here](https://hire.annedorko.com).

## Built With

- [TailwindCSS](https://github.com/tailwindlabs/tailwindcss)

## Getting Started

If you use this project base, modify this project to suit your own resume and portfolio activities!

### Prerequisites

Built and tested with:

- Python 3
- Node.js 15+
- NPM 7+

The program may work on lower versions of Node or NPM.

### Installation

1. Clone this repo into a clean project folder.
2. Install NPM packages.
3. Generate the site in the console using `python site.py`

Run `python site.py server` and navigate to [http://localhost:4242](http://localhost:4242) to preview your site live.

Run `python site.py watch` to regenerate the site automatically as you make changes to `/pages`, `/resume`, and `/templates`.

Run `python site.py compile` to compile the site using Tailwind CSS at production size.

### Usage

Modify target roles and professional summaries using `resume/roles.yaml`

Modify career history under `resume/history/`

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

### Resources
- [othneildrew’s Best README Template](https://github.com/othneildrew/Best-README-Template)
- [nqcm’s Static Site Generator Tutorial](https://github.com/nqcm/static-site-generator)
- [Ansible YAML Syntax Documentation](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)

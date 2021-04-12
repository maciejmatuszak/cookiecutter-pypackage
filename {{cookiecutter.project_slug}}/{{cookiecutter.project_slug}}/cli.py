{%- if cookiecutter.command_line_interface|lower == 'docopt' -%}
"""
Console script for {{cookiecutter.project_slug}}.
Example ussage of docopt https://github.com/docopt/docopt

Usage:
  cli ship new <name>...
  cli ship <name> move <x> <y> [--speed=<kn>]
  cli ship shoot <x> <y>
  cli mine (set|remove) <x> <y> [--moored|--drifting]
  cli -h | --help
  cli --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
"""
{%- else -%}
"""
Console script for {{cookiecutter.project_slug}}.
"""
{%- endif %}

{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
{%- endif %}
import sys
{%- if cookiecutter.command_line_interface|lower == 'click' %}
import click
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'docopt' %}
from docopt import docopt
import pkg_resources
__version__ = '{{ cookiecutter.version }}'
{%- endif %}
{% if cookiecutter.create_json_cli_config == 'y' %}
from {{cookiecutter.project_slug}}.config.CliConfig import CliConfig
{%- endif %}

{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}."""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    {% if cookiecutter.create_json_cli_config == 'y' %}config = CliConfig.getConfig(){% endif %}

    return 0
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
def main():
    """Console script for {{cookiecutter.project_slug}}."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "{{cookiecutter.project_slug}}.cli.main")

    {% if cookiecutter.create_json_cli_config == 'y' %}config = CliConfig.getConfig(){% endif %}
    return 0
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'docopt' %}
def main():
    arguments = docopt(__doc__, version=f'{__version__}')
    print(arguments)
    {% if cookiecutter.create_json_cli_config == 'y' %}config = CliConfig.getConfig(){% endif %}
    return 0
{%- endif %}


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

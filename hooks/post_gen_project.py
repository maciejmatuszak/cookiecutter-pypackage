#!/usr/bin/env python
import os
import shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath), )


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'n' in '{{ cookiecutter.create_json_cli_config|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'config')
        remove_dir(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

    if '{{ cookiecutter.create_git_repo }}' == 'y':
        subprocess.call(['git', 'init'], cwd=PROJECT_DIRECTORY)
        subprocess.call(['git', 'add', '*'], cwd=PROJECT_DIRECTORY)
        subprocess.call(['git', 'commit', '-m', 'Initial commit'], cwd=PROJECT_DIRECTORY)

#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages, Command
{%- if cookiecutter.create_json_cli_config == 'y' %}
import distutils
from distutils.command.build_py import build_py
import os
import subprocess
{% endif -%}

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    {% if cookiecutter.command_line_interface|lower == 'click' %}'Click>=7.0',{% endif %}
    {% if cookiecutter.command_line_interface|lower == 'docopt' %}'docopt>=0.6',{% endif %}
]

setup_requirements = [{%- if cookiecutter.use_pytest == 'y' %}'pytest-runner',{%- endif %} ]

test_requirements = [{%- if cookiecutter.use_pytest == 'y' %}'pytest>=3',{%- endif %} ]

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

{%- if cookiecutter.create_json_cli_config == 'y' %}
class BuildPyCommand(build_py):
    """Custom build command. just run build_cpp_lib before build_py"""

    def run(self):
        self.run_command('gen_code')
        build_py.run(self)

class GenJsonPopo(Command):
    """A custom command to run Pylint on all Python source files."""

    description = 'generate pojo classes based on json schema'
    user_options = [
        # The format is (long option, short option, description).
        ('json-schema=', None, 'path to json schema file'),
        ('use-types=', None, 'Add MyPy typings'),
        ('constructor-type-check=', None,
         'Validate provided types in constructor. Default only type checks when setting property values and not when setting them in the constructor.'),
        ('use-slots=', None, 'Add a __slots__ to each generated class to be more memory efficient.'),
        ('no-generate-from-definitions=', None,
         'Don\'t generate any classes from the "definitions" section of the schema.'),
        ('no-generate-from-root-object=', None, 'Don\'t generate any classes from the root of the schema.'),
        ('translate-properties=', None,
         'Translate property names to be snake_case. With this enabled, inner classes will no longer be prefixed by "_" since their names won\'t collide with the property name.'),
        ('language=', None, 'Language to generate in. Either "js" "go" or "python"'),
        ('namespace-path=', None, 'Namespace path to be prepended to the @memberOf for JSDoc (only used for JS)'),
        ('package-name=', None, 'Package name for generated code (only used for Go). Default is "generated"'),
        ('output-file=', None, 'output file name'),
        ('custom-template=', None, 'Jinja custom template'),
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)
        self.json_schema = ''
        self.use_types = ''
        self.constructor_type_check = ''
        self.use_slots = ''
        self.no_generate_from_definitions = ''
        self.no_generate_from_root_object = ''
        self.translate_properties = ''
        self.language = ''
        self.namespace_path = ''
        self.package_name = ''
        self.output_file = ''
        self.custom_template = ''

    def initialize_options(self):
        """Set default values for options."""
        self.json_schema = ''
        self.use_types = ''
        self.constructor_type_check = ''
        self.use_slots = ''
        self.no_generate_from_definitions = ''
        self.no_generate_from_root_object = ''
        self.translate_properties = ''
        self.language = ''
        self.namespace_path = ''
        self.package_name = ''
        self.output_file = ''
        self.custom_template = ''

    def finalize_options(self):
        """Post-process options."""
        if not self.json_schema:
            self.json_schema = '{{ cookiecutter.project_slug }}/config/cli_config_schema.json'

        if not self.custom_template:
            self.custom_template = '{{ cookiecutter.project_slug }}/config/python_class.jinja2'

        if not self.output_file:
            self.output_file = '{{ cookiecutter.project_slug }}/config/cli_config_models.py'

        assert os.path.exists(self.json_schema), (
                'Json schema file %s does not exists.' % self.json_schema)

    def run(self):
        """Run command."""

        command = ['jsonschema2popo2',
                   '--no-generate-from-root-object',
                   '--constructor-type-check',
                   '--use-types',
                   f'--custom-template={self.custom_template}',
                   f'--output-file={self.output_file}',
                   self.json_schema
                   ]
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        subprocess.check_call(command)

        self.announce(
            f'Generated: {self.language} file {self.output_file} from {self.json_schema}',
            level=distutils.log.INFO)

{% endif -%}
setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="{{ cookiecutter.project_short_description }}",
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main',
        ],
    },
    {%- endif %}
    install_requires=requirements,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(include=['{{ cookiecutter.project_slug }}', '{{ cookiecutter.project_slug }}.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
    cmdclass = {
        'gen_code': GenJsonPopo,
        'build_py': BuildPyCommand
    },
)

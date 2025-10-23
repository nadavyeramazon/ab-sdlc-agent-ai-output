"""Setup configuration for Hello World application."""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hello_world',
    version='0.1.0',
    description='A simple Hello World application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='AB SDLC Agent AI',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.13',
    classifiers=[
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
    ],
)

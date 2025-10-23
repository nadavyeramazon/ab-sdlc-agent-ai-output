"""Setup script for the Hello World application."""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hello-world-app',
    version='0.1.0',
    description='A sophisticated Hello World application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='AI Team',
    author_email='ai.team@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.13',
    install_requires=[
        'python-json-logger>=2.0.7',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pytest-mock>=3.11.1',
        ],
    },
    entry_points={
        'console_scripts': [
            'hello-world=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
    ],
)

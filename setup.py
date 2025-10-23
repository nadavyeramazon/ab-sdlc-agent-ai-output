"""Setup configuration for Hello World package."""

from setuptools import setup, find_packages

setup(
    name='hello-world',
    version='0.1.0',
    description='A production-grade Hello World application',
    author='AB SDLC Team',
    author_email='team@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.13',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pylint>=3.0.0',
            'mypy>=1.0.0',
        ],
    },
)

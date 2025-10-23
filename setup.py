"""Setup configuration for the Hello World package."""

from setuptools import setup, find_packages

setup(
    name='hello_world',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'hello-world=hello_world.main:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple Hello World application with logging',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/hello_world',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

from setuptools import setup, find_packages

setup(
    name='hello-world',
    version='1.0.0',
    description='A production-ready Hello World application',
    author='AI Agent',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'logging-utils>=2.0.0',
    ],
    extras_require={
        'test': [
            'coverage>=6.0.0',
            'flake8>=4.0.0',
            'mypy>=0.900',
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
    ],
)
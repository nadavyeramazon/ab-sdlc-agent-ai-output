from setuptools import setup, find_packages

setup(
    name="ab-sdlc-agent-ai-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Add production dependencies here
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-cov>=4.1.0',
        ],
    },
    python_requires='>=3.13',
    entry_points={
        'console_scripts': [
            'hello-world=src.main:main',
        ],
    },
)

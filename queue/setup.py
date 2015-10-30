try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Queue',
    'author': 'Saurabh Jinturkar',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['queue'],
    'scripts': [],
    'name': 'queue'
}

setup(**config)

try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

config = {
    'description' : 'Dead Simple',
    'author' : 'Leonard Lewis',
    'url' : 'https://github.com/leonardlewis/deadsimple',
    'download_url' : 'https://github.com/leonardlewis/deadsimple.git',
    'version' : '0.1',
    'install_requires' : ['pytest', 'twilio'],
    'packages' : ['deadsimple'],
    'scripts' : [],
    'name' : 'deadsimple'
}

setup(**config)

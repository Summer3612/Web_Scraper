from setuptools import setup, find_packages

setup(
    name='scraper',
    version='0.0.0',
    packages=find_packages(include=['Scraper','Scraper.*']),
    install_requires=[
        'urllib',
        'selenium', 
        'time',
        'json',
        'pandas',
         'uuid', 
        'os'

    ]
)
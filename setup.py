from setuptools import setup, find_packages

setup(
    name='scraper',
    version='2.0',
    packages=find_packages(include=['scraper','scraper.*']),
    install_requires=[
            'boto3',
            'selenium ==4.3.0', 
            'requests',
            'sqlalchemy',
            'pandas',
            'psycopg2-binary',
               ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
         )

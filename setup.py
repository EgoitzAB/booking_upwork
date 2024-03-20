# setup.py
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='booking_upwork',
    version='0.1.1',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'start=src.mex:main',
        ],
    },
)
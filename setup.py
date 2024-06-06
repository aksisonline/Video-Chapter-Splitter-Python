# Run the `setup.py` script to install the necessary dependencies.

from setuptools import setup, find_packages

setup(
    name='kaggle',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'moviepy'
    ]
)
"""Setup of program...
"""

from setuptools import setup, find_packages

setup(
    name="anime_automove",

    version="2.0.0",

    description="Organize anime from a drop folder to another one relying on fansub naming convention",

    author="SuperMiaw",

    #classifiers=[
    #
    #],

    python_requires='>=3',

    install_requires=[
        'sqlalchemy',
        'configobj'
    ],

    packages=find_packages(),
    include_package_data=True,

    entry_points={
       'console_scripts': [
           'anime_automove=anime_automove:main',
       ],
    },
)

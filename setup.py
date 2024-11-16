from setuptools import setup, find_packages
setup(
    name='pws256',
    version='1.1.0',
    description="pws256: A module that is used for users and passwords, and also has validation methods to check passwords with strings",
    packages=find_packages(include=["*"], exclude=["_setup", "src", ".github", "srcimport", "usersrcimport"]),
    author='Hector Robertson'
)
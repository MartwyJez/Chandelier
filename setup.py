from setuptools import setup

setup(
   name='Chandelier',
   version='1.0',
   description='Software to operate artistic installation in form of Chandelier',
   author='Arkadiusz Kotwica',
   author_email='arkadiusz.kotwica1@gmail.com',
   packages=['chandelier'],  #same as name
   install_requires=['retry', 'RPi.GPIO'], #external packages as dependencies
)

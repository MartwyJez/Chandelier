from setuptools import setup, setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='Chandelier',
    version='1.0',
    description='Software to operate artistic installation in form of Chandelier',
    author='Arkadiusz Kotwica',
    author_email='arkadiusz.kotwica1@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Raspbian Buster",
    ],
    packages=setuptools.find_packages(),  #same as name
    install_requires=['retry', 'RPi.GPIO', 'pydub', 'evdev', 'asyncio', 'pexpect', 'pulsectl', 'python-vlc'], #external packages as dependencies
    python_requires='>=3.7',
)

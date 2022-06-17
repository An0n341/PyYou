from setuptools import setup, find_packages

with open("README.md") as file:
    long_description = file.read()

with open("LICENSE") as file:
    license = file.read()

setup(
    name="PyYou",
    version="1.0",
    description="PyYou is a minimal desktop application to download any YouTube video/playlist. With the ability to select how to download the video (video or audio)",
    long_description=long_description,
    author="Anon",
    url="https://github.com/An0n341/PyYou",
    license=license,
    packages=find_packages(exclude=("tests", "docs"))
)
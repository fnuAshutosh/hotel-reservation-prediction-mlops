from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name = "Hotel_reservation_prediction",
    version = "0.0.1",
    author="Fnu Ashutosh",
    packages=find_packages(),
    install_requires=required
)
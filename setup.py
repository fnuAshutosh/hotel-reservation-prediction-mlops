from setuptools import setup,find_packages

def read_requirements(filename):
    with open(filename, encoding='utf-8-sig') as f:
        lines = f.read().splitlines()
    # Filter out empty lines and comments
    return [line.strip() for line in lines if line.strip() and not line.startswith('#')]

requirements = read_requirements("requirements.txt")

setup(
    name = "Hotel_reservation_prediction",
    version = "0.0.1",
    author="Fnu Ashutosh",
    packages=find_packages(),
    install_requires = requirements,
)
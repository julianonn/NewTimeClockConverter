from setuptools import setup, find_packages



with open('LICENSE') as f:
    license = f.read()

setup(
    name='NewTimeClockConverter',
    version='0.1dev',
    description='Payroll CSV converter',
    author='Julia Nonnenkamp',
    url='https://github.com/julianonn/NewTimeClockConverter',
    license=license,
    packages=find_packages()
)
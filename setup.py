from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='rciam-federation-registry-agent',
    author='grnet',
    author_email='faai@grnet.gr',
    version='2.2.0',
    license='ASL 2.0',
    url='https://github.com/rciam/rciam-federation-registry-agent',
    packages=find_packages(),
    scripts=['bin/deployer_ssp','bin/deployer_mitreid','bin/deployer_keycloak'],
    zip_safe=False,
    install_requires=install_requires,
    dependency_links=dependency_links,
    description='A library that connects to ams using argo-ams-library and syncs with MITREid, SimpleSAMLphp and Keycloak',
    long_description = long_description,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: PHP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)

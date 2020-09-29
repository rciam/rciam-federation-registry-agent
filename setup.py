import os
from setuptools import setup, find_packages

setup(
    name='rciam-service-registry-agent',
    author='grnet',
    author_email='faai@grnet.gr',
    version='1.0.0',
    license='ASL 2.0',
    url='https://github.com/rciam/rciam-service-registry-agent',
    packages=find_packages(),
    scripts=['bin/deployer_ssp'],
    zip_safe=False,
    description='A library that connects to ams using argo-ams-library and syncs with mitrID and ssp',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: PHP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pozetron-barcode',
    description='A microservice to generate barcodes (QR codes) for arbitrary strings.',
    version=':versiontools:pozetron_barcode:',

    packages=find_packages(),
    include_package_data=True,
    setup_requires=('versiontools'),

    author='Pozetron Inc',
    author_email='admin@pozetroninc.com',
    url='www.pozetron.com',
)

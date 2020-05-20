from setuptools import setup

with open('requirements.txt', 'r') as fp:
    requirements = fp.read().splitlines()

setup(
    name='pya2l',
    version='0.0.1',
    packages=[
        'pya2l',
        'pya2l.a2l',
        'pya2l.a2ml',
        'pya2l.parser',
        'pya2l.shared',
        'pya2l.parser.grammar'
    ],
    url='https://github.com/Sauci/pya2l',
    license='BSD',
    author='Guillaume Sottas',
    author_email='guillaumesottas@gmail.com',
    description='utility for a2l files',
    entry_points={
        'console_scripts': [ 'pya2l=pya2l:main' ]
    },
    long_description='this package provides an API to access different nodes in an a2l-formatted file',
    install_requires=requirements,
    dependency_links=[
        'https://pypi.python.org/packages/e5/69/882ee5c9d017149285cab114ebeab373308ef0f874fcdac9beb90e0ac4da/ply-3.11.tar.gz#md5=6465f602e656455affcd7c5734c638f8'
    ]
)

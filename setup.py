from setuptools import setup

setup(
    name='pya2l',
    version='0.0.11',
    packages=['pya2l', 'pya2l.parser', 'pya2l.parser.grammar'],
    url='',
    license='BSD',
    author='Guillaume Sottas',
    author_email='guillaumesottas@gmail.com',
    description='utility for a2l files',
    install_requires='ply',
    dependency_links=[
        'https://pypi.python.org/packages/e5/69/882ee5c9d017149285cab114ebeab373308ef0f874fcdac9beb90e0ac4da/ply-3.11.tar.gz#md5=6465f602e656455affcd7c5734c638f8'
    ],
    package_data={
        '': ['pya2l/parser/grammar/parser.out',
             'pya2l/parser/grammar/parsetab.py']
    },
    include_package_data=True,
)

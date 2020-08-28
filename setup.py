"""
When packaging LTF software, as libraires, or applications
this is the setup.py template that should be used
"""
from setuptools import setup, find_packages

# constantants that should be front and center
VERSION = '0.0.1'
LICENSE = 'BSD 2-Clause'
PKG_NAME = 'chroma_blend'
REPO_URL = 'https://github.com/JohannSuarez/chroma_blend'
EMAIL = 'johann.suarez92@gmail.com'


with open('README.md', 'r') as fh:
    long_description = fh.read()

# much better way to source dependencies, load in
# requirements.txt, so we only have to maintain the onefile
# instead of two, and the requirements will be installed automatically
# when the package is pip installed
with open('requirements.txt') as depends:
    requirements = depends.read().splitlines()

setup(
    name=PKG_NAME,
    version=VERSION,
    install_requires=requirements,
    author="Johann Suarez",
    author_email=EMAIL,
    description="Example Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=REPO_URL,
    license=LICENSE,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
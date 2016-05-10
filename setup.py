from setuptools import setup, find_packages
import sys

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'cifsdk/_version.py'
versioneer.versionfile_build = 'cifsdk/_version.py'
versioneer.tag_prefix = ''  # tags are like 1.2.0
versioneer.parentdir_prefix = 'py-cifsdk-'  # dirname like 'myproject-1.2.0'

cmds = [
    "cif=cifsdk.client:main",
]

try:
    import cgmail
    cmds.append('cgmail-cif=cifsdk.cifcgmail:main')
except ImportError:
    pass

try:
    import elasticsearch
    cmds.append('cif-es-reindex=cifsdk.extras.es_reindex:main')
except ImportError:
    pass

setup(
    name="cifsdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CIF Python SDK",
    long_description="CIF Software Development Kit for Python",
    url="https://github.com/csirtgadgets/cif-sdk-py",
    license='LGPL3',
    classifiers=[
       "Topic :: System :: Networking",
       "Environment :: Other Environment",
       "Intended Audience :: Developers",
       "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
       "Programming Language :: Python",
       ],
    keywords=['cif', ' security'],
    author="Wes Young",
    author_email="wes@barely3am.com",
    packages=find_packages(),
    install_requires=reqs,
    entry_points={
          'console_scripts': cmds
      },
    test_suite="test"
)

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'cifsdk/_version.py'
versioneer.versionfile_build = 'cifsdk/_version.py'
versioneer.tag_prefix = ''  # tags are like 1.2.0
versioneer.parentdir_prefix = 'py-cifsdk-'  # dirname like 'myproject-1.2.0'

setup(
    name="py-cifsdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CIF Python SDK",
    long_description="CIF Software Development Kit for Python",
    url="https://github.com/csirtgadgets/py-cifsdk",
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
          'console_scripts': [
              "cif=cifsdk.client:main",
              "cif-procmail=cifsdk.procmail:main"
              ]
      },
    test_suite="test"
)

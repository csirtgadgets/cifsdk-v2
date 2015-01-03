from setuptools import setup

import cif.sdk
setup(
      name="cif-sdk",
      version=cif.sdk.__version__,
      description="CIF Python SDK",
      long_description="CIF Software Development Kit for Python",
      url="https://github.com/csirtgadgets/py-cif-sdk",
      license='LGPL3',
      classifiers=[
                   "Topic :: System :: Networking",
                   "Environment :: Other Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
                   "Programming Language :: Python",
                   ],
      keywords=['cif','security','intelligence'],
      author="Wes Young",
      author_email="wes@barely3am.com",
      packages = ["cif","cif.sdk","test"],
      install_requires = ["requests>=2.0"
                          "json",
                          'pyyaml',
                          'prettytable',
                          'ujson'],
      scripts=['bin/cif'],
      test_suite = "test"
)

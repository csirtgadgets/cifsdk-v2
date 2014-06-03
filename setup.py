from setuptools import setup
 
import cif.sdk

setup(name="cif-sdk",
    version=cif.sdk.__version__,
    description="CIF Python SDK",
    long_description="CIF Software Development Kit for Python",
    url="https://github.com/csirtgadgets/cif-sdk-python",
    license='LGPL',
    classifiers=[
        "Topic :: System :: Networking",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: LGPL License",
        "Programming Language :: Python",
    ],
    keywords='CIF',
    author="Wes Young",
    author_email="wes@barely3am.com",
    packages = ["cif.sdk","test"],
    install_requires = [
        "requests>=2.0"
        "json",
    ],
    scripts=['bin/cif'],
    test_suite = "test"
)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="cif-sdk",
    version="0.1",
    description="CIF Python SDK",
    long_description="",
    url="https://github.com/csirtgadgets/cif-sdk-python",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    classifiers=[
        "Topic :: System :: Networking",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    keywords='CIF',
    author="Wes Young",
    author_email="wes@barely3am.com",
    packages = ["cif",
                "cif.sdk",
                "cif.sdk.Client"],
    install_requires = [
        "requests>=2.0"
    ],
    scripts=['bin/cifpy'],
)

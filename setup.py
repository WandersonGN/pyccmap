from setuptools import setup

DEPENDENCIES = open("requirements.txt", "r").read().split("\n")
README = open("README.md", "r").read()

setup(name = "pyccmap",
      version = "0.1.1",
      description = "Python library and command-line utility to work with values of multiple cryptocurrencies from multiple exchanges.",
      long_description = README,
      long_description_content_type = "text/x-md",
      author = "",
      author_email = "",
      url = "https://github.com/Notjack429/pyccmap",
      packages = ["pyccmap", "pyccmap.apis"],
      entry_points = {"console_scripts": ["pyccmap=pyccmap.__main__:main"]},
      install_requires = DEPENDENCIES,
      keywords = ["security", "network"])

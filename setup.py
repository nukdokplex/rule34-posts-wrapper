import os.path

from setuptools import setup, find_packages

here = os.path.dirname(__file__)

description_file = os.path.join(here, "README.md")
version_file = os.path.join(here, "src", "rule34_posts_wrapper", "__version__.py")

version_info = {}
with open(version_file, "r") as f:
    exec(f.read(), version_info)

dev_requirements = ["coverage", "pytest", "pytest-cov", "pre-commit", "coverage", "tox"]

setup(
    name=version_info["__title__"],
    version=version_info["__version__"],
    packages=find_packages("src", exclude=["test"]),
    package_dir={"": "src"},
    url="https://github.com/nukdokplex/rule34-posts-wrapper",
    license="MIT",
    author="NukDokPlex",
    author_email="nukdokpelx@outlook.com",
    description="Library for retrieving posts and tags from rule34.paheal.net",
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r").read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia",
        "Topic :: Games/Entertainment",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "lxml", "beautifulsoup4", "soupsieve", "urllib3"],
    extras_require={"development": dev_requirements},
)

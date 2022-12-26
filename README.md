# Rule34 posts wrapper
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/nukdokplex/rule34-posts-wrapper/.github/workflows/ci.yml?label=CI&logo=github&branch=master)](https://github.com/nukdokplex/rule34-posts-wrapper/actions/workflows/ci.yml)
[![Codecov](https://img.shields.io/codecov/c/gh/nukdokplex/rule34-posts-wrapper?token=FZ6UNF6GE1&label=tests%20coverage)](https://app.codecov.io/gh/nukdokplex/rule34-posts-wrapper)
[![GitHub Repo stars](https://img.shields.io/github/stars/nukdokplex/rule34-posts-wrapper)](https://github.com/nukdokplex/rule34-posts-wrapper)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/Rule34-Posts-Wrapper?label=PyPI%20d-loads%3A)](https://pypi.org/project/Rule34-Posts-Wrapper/)

This is a [rule34.paheal.net](https://rule34.paheal.net) wrapper that turns your query into an iterable list of posts
with the most important information about them.

## Installation

To install:
```shell
pip install rule34-posts-wrapper
```
Or for development/testing purposes, clone and run:
```shell
pip install -e .[development]
pre-commit install
```

## Usage

### PostsWrapper

To start import ``PostsWrapper`` and call it:
```python
from rule34_posts_wrapper import PostsWrapper

posts = PostsWrapper(['your', 'query', 'here'])[0].file
```

Note that there is **no authentication** for now so you can't use more than three tags in your query.

Now you can iterate the posts in cycle:
```python
for post in posts:
    print(str(post.file) + " - " + " ".join(post.tags)) # Do whatever you want with Post object
```

Also you can just interact with it like ``list``

```python
first_post = posts[0]
print(str(first_post.thumbnail))
```
Note that all URLs are ``urllib3.util.Url``, call ``str(posts[x].link)`` to convert it to ``str``.

### TagsWrapper

Like ``PostsWrapper``, ``TagsWrapper`` provides you iterable list of ``Tag``'s:

```python
from rule34_posts_wrapper import TagsWrapper

tags = TagsWrapper("Your_Query_Here")

print(f"Found {len(tags)} tags:", end="\n\n")
for tag in tags:
    print(f"Tag: {tag.name}, Count: {tag.count}")
```

It uses [rule34.paheal.net](https://rule34.paheal.net) autocomplete that helps you find tags by it's starting
substring.

## Testing

To run all tests, just use this command:
```shell
tox -e py
```

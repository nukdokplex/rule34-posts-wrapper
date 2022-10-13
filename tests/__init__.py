import os

from rule34_posts_wrapper.posts_wrapper import PostsWrapper
from rule34_posts_wrapper.tags_wrapper import TagsWrapper
from rule34_posts_wrapper.utils import is_safe_string, is_list_of_safe_strings

post_query = os.environ.get("RULE34_POST_TAGS")
tag_query = os.environ.get("RULE34_TAG_QUERY")

if not post_query:
    post_query = input("Enter posts query: ")
if not tag_query:
    tag_query = input("Enter tag query: ")

post_query = post_query.split(' ')

if not is_list_of_safe_strings(post_query):
    raise ValueError("post query should be a list of strings, each of which should consist of letters, numbers, "
                     "dashes, underscores and apostrophes")

if not is_safe_string(tag_query):
    raise ValueError("tag query must consist of letters, numbers, dashes, underscores and apostrophe")

posts_wrapper = PostsWrapper(post_query)
tags_wrapper = TagsWrapper(tag_query)

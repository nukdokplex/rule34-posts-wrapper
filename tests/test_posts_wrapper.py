from unittest import TestCase

from rule34_posts_wrapper import PostsWrapper
from tests import posts_wrapper

bad_queries = [[" ", ",", "asd,asd f"]]

good_queries = [["asd", "dsa"], ["sk^yr@im"], ["123_321'-"]]


class TestPostsWrapper(TestCase):
    def test_iterator(self):
        """Tests iterator of Posts Wrapper."""
        count = 0
        for _ in posts_wrapper:
            count += 1

        assert count == len(posts_wrapper), "Posts Wrapper's len() is not actual count"

    def test_bad_query(self):
        """Tests Posts Wrapper's bad query validation."""
        for bad_query in bad_queries:
            with self.assertRaises(ValueError):
                PostsWrapper(bad_query)

    def test_good_queries(self):
        """Tests Posts Wrapper's good query validation."""
        for good_query in good_queries:
            try:
                PostsWrapper(good_query)
            except ValueError as e:
                self.fail(
                    f"Test failed at \"{' '.join(good_query)}\" query with exception: {str(e)}"
                )

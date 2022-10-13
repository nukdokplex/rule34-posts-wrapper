from unittest import TestCase

from rule34_posts_wrapper.tags_wrapper import TagsWrapper
from tests import tags_wrapper

bad_queries = ["awshnhbf*sdgn_er=", "sdf."]

good_queries = ["asd", "dsa", "sky", "2", "leag(", ""]


class TestTagsWrapper(TestCase):
    def test_iterator(self):
        """Tests iterator of Tags Wrapper."""
        count = 0
        for _ in tags_wrapper:
            count += 1
        assert count == len(tags_wrapper), "Tags Wrapper's len() is not actual count"

    def test_bad_query(self):
        """Tests Tags Wrapper's bad query validation."""
        for bad_query in bad_queries:
            with self.assertRaises(ValueError) as cm:
                TagsWrapper(bad_query)

    def test_good_queries(self):
        """Tests Posts Wrapper's good query validation."""
        for good_query in good_queries:
            try:
                TagsWrapper(good_query)
            except ValueError as e:
                self.fail(
                    f"Test failed at \"{' '.join(good_query)}\" query with exception: {str(e)}"
                )

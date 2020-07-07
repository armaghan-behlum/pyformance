class BaseMetric(object):

    """
    Abstract class for grouping common properties of metrics, such as tags
    """

    def __init__(self, key, tags=None):
        # can't have spaces or commas in metric name
        # okay to have in tags
        self.key = self._clean(key)
        self.tags = tags or {}

    def _clean(self, value: str):
        if value:
            return value.replace(" ", "_").replace(",", "_")
        else:
            return None

    def get_tags(self):
        return self.tags

    def get_key(self):
        return self.key

    def __hash__(self):
        if not self.tags:
            return hash(self.key)

        return hash((self.key, frozenset(self.tags.items())))

    def __eq__(self, other):
        if not isinstance(other, BaseMetric):
            return False

        return self.key == other.key and set(self.tags) == set(other.tags)
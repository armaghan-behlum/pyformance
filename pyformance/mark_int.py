class MarkInt:
    """
    Mark metric value as and integer.

    Reporters such as influx require consistent data types for metrics and require you
    to mark integer values with an "i" suffix. This is here to let Influx know it should
    do so for the value it's initialized with.
    """
    def __init__(self, value):
        self.value = int(value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"MarkInt({self.value})"

    def __eq__(self, other):
        return isinstance(other, MarkInt) and other.value == self.value

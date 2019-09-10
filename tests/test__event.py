from pyformance.meters import Event, EventPoint
from tests import TimedTestCase


class EventTestCase(TimedTestCase):
    def setUp(self):
        super(EventTestCase, self).setUp()
        self.event = Event(
            clock=TimedTestCase.clock,
            key="test_event",
            tags={"name", "value"}
        )

    def tearDown(self):
        super(EventTestCase, self).tearDown()

    def test_add_event_and_read_it(self):
        mock_values = {"value": 1}

        self.event.add(mock_values)

        events = self.event.get_events()
        self.assertEqual(events, [EventPoint(
            time=self.clock.time(),
            values=mock_values
        )])

    def test_clear_event_clears_events(self):
        self.event.add({"value": 1})

        self.event.clear()
        self.assertEqual(len(self.event.get_events()), 0)

    def test_get_event_returns_shallow_copy(self):
        mock_values = {"value": 1}

        self.event.add(mock_values)

        events = self.event.get_events()
        self.assertEqual(len(events), 1)

        # make sure the returned object is not a reference(important for thread safety)
        self.event.clear()
        self.assertEqual(len(events), 1)

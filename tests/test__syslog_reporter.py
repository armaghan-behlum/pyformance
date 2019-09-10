from unittest import mock

from pyformance import MetricsRegistry
from pyformance.reporters.syslog_reporter import SysLogReporter
from tests import TimedTestCase


class TestSysLogReporter(TimedTestCase):
    def setUp(self):
        super(TestSysLogReporter, self).setUp()
        self.registry = MetricsRegistry(clock=self.clock)
        self.maxDiff = None
        self.clock.now = 0

    def tearDown(self):
        super(TestSysLogReporter, self).tearDown()
        self.clock.now = 0

    def test_report_now(self):
        # connect to a local rsyslog server
        r = SysLogReporter(
            registry=self.registry, reporting_interval=1, clock=self.clock
        )
        h1 = self.registry.histogram("hist")
        for i in range(10):
            h1.add(2 ** i)
        gcb = self.registry.gauge("gcb", lambda: 123)
        gsimple = self.registry.gauge("gsimple").set_value(42)
        t1 = self.registry.timer("t1")
        m1 = self.registry.meter("m1")
        m1.mark()
        e1 = self.registry.event("e1")
        e1.add({"field": 1})
        with t1.time():
            c1 = self.registry.counter("c1")
            c2 = self.registry.counter("counter-2")
            c1.inc()
            c2.dec()
            c2.dec()
            self.clock.add(1)
        with mock.patch(
                "pyformance.reporters.syslog_reporter.logging.Logger.info"
        ) as patch:
            r.report_now()

            self.assertEqual(patch.call_count, 2)
            calls = patch.call_args_list

            expected = (
                '{"c1.count": 1, "counter-2.count": -2, '
                '"gcb.value": 123, "gsimple.value": 42, '
                '"hist.75_percentile": 160.0, "hist.95_percentile": 512, '
                '"hist.999_percentile": 512, "hist.99_percentile": 512, '
                '"hist.avg": 102.3, "hist.count": 10.0, "hist.max": 512, '
                '"hist.min": 1, "hist.std_dev": 164.94851048466944, '
                '"m1.15m_rate": 0, "m1.1m_rate": 0, "m1.5m_rate": 0, "m1.count": 1.0, '
                '"m1.mean_rate": 1.0, "t1.15m_rate": 0, "t1.1m_rate": 0, '
                '"t1.50_percentile": 1, "t1.5m_rate": 0, "t1.75_percentile": 1, '
                '"t1.95_percentile": 1, "t1.999_percentile": 1, "t1.99_percentile": 1, '
                '"t1.avg": 1.0, "t1.count": 1.0, "t1.max": 1, "t1.mean_rate": 1.0, '
                '"t1.min": 1, "t1.std_dev": 0.0, "t1.sum": 1.0, "timestamp": 1}'
            )

            # First call should be event free because events are reported based on submission
            # rather than report timestamp. And a single line contains a single timestamp.
            self.assertEqual(calls[0][0][0], expected)

            # Second call should only be events
            self.assertEqual(calls[1][0][0], '{"e1.field": 1, "timestamp": 0}')


if __name__ == "__main__":
    import unittest

    unittest.main()

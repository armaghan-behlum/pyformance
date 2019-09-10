# -*- coding: utf-8 -*-
import json
import logging
import logging.handlers
import socket
import sys

from six import iteritems

from .reporter import Reporter

DEFAULT_SYSLOG_ADDRESS = "/dev/log"
DEFAULT_SYSLOG_SOCKTYPE = socket.SOCK_DGRAM
DEFAULT_SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_USER


class SysLogReporter(Reporter):
    """
    Syslog is a way for network devices to send event messages to a logging server
    """

    def __init__(
            self,
            registry=None,
            reporting_interval=5,
            tag="pyformance",
            clock=None,
            address=DEFAULT_SYSLOG_ADDRESS,
            socktype=DEFAULT_SYSLOG_SOCKTYPE,
            facility=DEFAULT_SYSLOG_FACILITY,
    ):
        super(SysLogReporter, self).__init__(registry, reporting_interval, clock)

        handler = logging.handlers.SysLogHandler(
            address=address, facility=facility, socktype=socktype
        )
        handler.append_nul = False

        if tag is not None and tag != "":
            if sys.version_info >= (3, 3):
                handler.ident = tag + ": "
            else:
                formatter = logging.Formatter("{}: %(message)s".format(tag))
                handler.setFormatter(formatter)

        logger = logging.getLogger("pyformance")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        self.logger = logger

    def report_now(self, registry=None, timestamp=None):
        registry = registry or self.registry
        metric_data = registry.dump_metrics()

        metrics = self._collect_metrics(metric_data, timestamp)
        if metrics:
            self.logger.info(metrics)

        for metrics in self._collect_events(metric_data):
            self.logger.info(metrics)

    def _collect_events(self, metrics):
        for metric_name, metric in iteritems(metrics):
            if metric.get("events"):
                for event in metric["events"]:
                    metrics_data = {"timestamp": event.time}

                    for field_name, value in event.values.items():
                        metrics_data[f"{metric_name}.{field_name}"] = value

                    yield json.dumps(metrics_data, sort_keys=True)

    def _collect_metrics(self, metrics, timestamp=None):
        timestamp = timestamp or int(round(self.clock.time()))

        metrics_data = {"timestamp": timestamp}
        for metric_name, metric in iteritems(metrics):
            for metric_key, metric_value in iteritems(metric):
                # Exclude events from here, require special handling
                if metric_key != "events":
                    metrics_data["{}.{}".format(metric_name, metric_key)] = metric_value
        result = json.dumps(metrics_data, sort_keys=True)

        return result

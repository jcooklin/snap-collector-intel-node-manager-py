#!/usr/bin/env python

from ceilometer.ipmi.platform.intel_node_manager import NodeManager as nm
import snap_plugin.v1 as snap


class NodeManager(snap.Collector):

    def __init__(self, name, version, **kwargs):
        self._nm = nm()
        super(NodeManager, self).__init__(name, version, **kwargs)

    def collect(self, metrics):
        for metric in metrics:
            if metric.namespace[2].value == "temperature" and \
                    metric.namespace[3].value == "inlet" and \
                    metric.namespace[4].value == "current":
                metric.data = int(self._nm.read_inlet_temperature()["Current_value"][0], 16)
            elif metric.namespace[2].value == "temperature" and \
                    metric.namespace[3].value == "inlet" and \
                    metric.namespace[4].value == "average":
                metric.data = int(self._nm.read_inlet_temperature()["Average_value"][0], 16)
            elif metric.namespace[2].value == "power" and \
                    metric.namespace[3].value == "system" and \
                    metric.namespace[4].value == "average":
                metric.data = int(self._nm.read_power_all()["Average_value"][0], 16)
            elif metric.namespace[2].value == "power" and \
                    metric.namespace[3].value == "system" and \
                    metric.namespace[4].value == "current":
                metric.data = int(self._nm.read_power_all()["Current_value"][0], 16)
        return metrics

    def update_catalog(self, config):
        return [
            snap.Metric(
                namespace=("intel", "dcm", "temperature", "inlet", "current"),
                description="inlet current temperature",
                unit="celsius"
            ),
            snap.Metric(
                namespace=("intel", "dcm", "temperature", "inlet", "average"),
                description="inlet average temperature",
                unit="celsius"
            ),
            snap.Metric(
                namespace=("intel", "dcm", "power", "system", "current"),
                description="current power",
                unit="watt"
            ),
            snap.Metric(
                namespace=("intel", "dcm", "power", "system", "average"),
                description="average power",
                unit="watt"
            )
        ]

    def get_config_policy(self):
        return snap.ConfigPolicy()

if __name__ == "__main__":
    NodeManager("dcm-py", 1).start_plugin()

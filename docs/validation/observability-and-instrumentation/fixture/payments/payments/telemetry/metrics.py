"""Counters, gauges and histograms. flush() merges this process's values into
var/telemetry/metrics.json, the way the metrics backend accumulates them."""
import json

from payments.paths import TELEMETRY

_REGISTRY = {}


def _key(labels):
    return json.dumps(labels, sort_keys=True)


class _Metric:
    kind = ""

    def __init__(self, name, help, labelnames=()):
        self.name, self.help, self.labelnames = name, help, tuple(labelnames)
        self.series = {}
        _REGISTRY[name] = self

    def _labels(self, kw):
        if set(kw) != set(self.labelnames):
            raise ValueError(f"{self.name} expects labels {self.labelnames}, got {sorted(kw)}")
        return _key(kw)


class Counter(_Metric):
    kind = "counter"

    def inc(self, amount=1, **labels):
        key = self._labels(labels)
        self.series[key] = self.series.get(key, 0) + amount


class Gauge(_Metric):
    kind = "gauge"

    def set(self, value, **labels):
        self.series[self._labels(labels)] = value


class Histogram(_Metric):
    kind = "histogram"

    def __init__(self, name, help, labelnames=(),
                 buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1)):
        super().__init__(name, help, labelnames)
        self.buckets = tuple(buckets)

    def observe(self, value, **labels):
        key = self._labels(labels)
        s = self.series.setdefault(key, {"count": 0, "sum": 0.0,
                                         "buckets": {str(b): 0 for b in self.buckets}})
        s["count"] += 1
        s["sum"] += value
        for b in self.buckets:
            if value <= b:
                s["buckets"][str(b)] += 1


def flush():
    TELEMETRY.mkdir(parents=True, exist_ok=True)
    path = TELEMETRY / "metrics.json"
    stored = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for name, metric in _REGISTRY.items():
        entry = stored.setdefault(name, {"kind": metric.kind, "help": metric.help, "series": {}})
        for key, value in metric.series.items():
            old = entry["series"].get(key)
            if metric.kind == "counter":
                entry["series"][key] = (old or 0) + value
            elif metric.kind == "gauge" or old is None:
                entry["series"][key] = value
            else:
                old["count"] += value["count"]
                old["sum"] += value["sum"]
                for b, n in value["buckets"].items():
                    old["buckets"][b] = old["buckets"].get(b, 0) + n
        metric.series = {}
    path.write_text(json.dumps(stored, indent=1, sort_keys=True), encoding="utf-8")

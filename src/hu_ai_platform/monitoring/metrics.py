"""Application metrics — token usage, latency, guardrail triggers."""

import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class RequestMetrics:
    """Metrics for a single request."""

    latency_ms: float = 0.0
    tokens_input: int = 0
    tokens_output: int = 0
    guardrail_triggered: bool = False
    guardrail_type: str | None = None


class MetricsCollector:
    """In-memory metrics collector for the demo."""

    def __init__(self) -> None:
        self.total_requests: int = 0
        self.total_tokens_input: int = 0
        self.total_tokens_output: int = 0
        self.guardrail_triggers: dict[str, int] = defaultdict(int)
        self._latencies: list[float] = []

    def record(self, metrics: RequestMetrics) -> None:
        """Record metrics from a completed request."""
        self.total_requests += 1
        self.total_tokens_input += metrics.tokens_input
        self.total_tokens_output += metrics.tokens_output
        self._latencies.append(metrics.latency_ms)

        if metrics.guardrail_triggered and metrics.guardrail_type:
            self.guardrail_triggers[metrics.guardrail_type] += 1

    @property
    def avg_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)

    def summary(self) -> dict[str, object]:
        return {
            "total_requests": self.total_requests,
            "total_tokens": {
                "input": self.total_tokens_input,
                "output": self.total_tokens_output,
            },
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "guardrail_triggers": dict(self.guardrail_triggers),
        }


@dataclass
class Timer:
    """Context manager for timing operations."""

    elapsed_ms: float = 0.0
    _start: float = field(default=0.0, repr=False)

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args: object) -> None:
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000

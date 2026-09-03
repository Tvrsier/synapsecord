from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ReadyState:
    expected: set[str] = field(default_factory=set)
    ready: set[str] = field(default_factory=set)

    def register(self, component: str) -> None:
        self.expected.add(component)

    def mark_ready(self, component: str) -> None:
        if component not in self.expected:
            raise ValueError(f"Unknown ready component: {component}")

        self.ready.add(component)

    @property
    def is_ready(self) -> bool:
        return self.expected == self.ready

    @property
    def pending(self) -> set[str]:
        return self.expected - self.ready
from dataclasses import dataclass

@dataclass(frozen=True)
class GestureState:
    """
    Represents the current interpreted gesture state.
    """

    name: str | None
    previous_name: str | None
    confidence: float
    duration: float
    changed: bool

    @property
    def is_active(self) -> bool:
        return self.name is not None

    @property
    def was_changed(self) -> bool:
        return self.changed

    def is_gesture(self, gesture_name: str) -> bool:
        return self.name == gesture_name

    def changed_to(self, gesture_name: str) -> bool:
        return self.changed and self.name == gesture_name

    def changed_from_to(self, previous_name: str, current_name: str) -> bool:
        return (
            self.changed
            and self.previous_name == previous_name
            and self.name == current_name
        )

    def held_for(self, seconds: float) -> bool:
        return self.duration >= seconds
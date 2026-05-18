"""Tests for MediaPipe gesture result interpretation."""

from dataclasses import dataclass

from gestures.gesture_interpreter import GestureInterpreter


@dataclass
class Category:
    category_name: str
    score: float


class Result:
    def __init__(self, gestures):
        self.gestures = gestures


def test_returns_none_when_result_is_missing():
    interpreter = GestureInterpreter()

    assert interpreter.interpret_gesture(None) == (None, 0.0)


def test_filters_low_confidence_gestures():
    interpreter = GestureInterpreter(min_confidence=0.8)
    result = Result([[Category("Pointing_Up", 0.7)]])

    assert interpreter.interpret_gesture(result) == (None, 0.7)


def test_returns_top_gesture_when_confident():
    interpreter = GestureInterpreter(min_confidence=0.5)
    result = Result([[Category("Open_Palm", 0.9)]])

    assert interpreter.interpret_gesture(result) == ("Open_Palm", 0.9)


def test_returns_none_when_gesture_lists_are_empty():
    interpreter = GestureInterpreter(min_confidence=0.5)
    result = Result([[]])

    assert interpreter.interpret_gesture(result) == (None, 0.0)

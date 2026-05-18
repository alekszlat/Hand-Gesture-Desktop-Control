import tkinter as tk
from tkinter import ttk

from gestures.mode_manager import AppMode


MODE_COMMANDS = {
    AppMode.BASE: [
        ("Move hand", "Move cursor"),
        ("Pointing_Up", "Left click"),
        ("Closed_Fist", "Enter drag mode"),
        ("Hold Thumb_Up", "Open launcher mode"),
        ("Hold ILoveYou", "Confirm close mode"),
    ],
    AppMode.DRAG: [
        ("Closed_Fist", "Hold mouse button"),
        ("Open_Palm", "Release and return to base"),
    ],
    AppMode.LAUNCHER: [
        ("ILoveYou", "Open browser"),
        ("Pointing_Up", "Open Discord"),
        ("Victory", "Open VS Code"),
        ("Closed_Fist", "Cancel launcher"),
    ],
    AppMode.CONFIRM_CLOSE: [
        ("Pointing_Up", "Close active window"),
        ("Closed_Fist", "Close gesture app"),
        ("Thumb_Up", "Cancel close"),
    ],
}


class StatusWidget:
    def __init__(self):
        self.closed = False
        self.root = tk.Tk()
        self.root.title("MBH Commands")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._keep_open)

        self.mode_value = tk.StringVar(value="BASE")
        self.gesture_value = tk.StringVar(value="None")

        self.command_rows: list[tuple[ttk.Label, ttk.Label]] = []

        self._build()

    def update(self, mode: AppMode, gesture_name: str | None) -> None:
        if self.closed:
            return

        self.mode_value.set(mode.value)
        self.gesture_value.set(gesture_name or "None")
        self._set_commands(MODE_COMMANDS.get(mode, []))

        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            self.closed = True

    def destroy(self) -> None:
        if self.closed:
            return

        try:
            self.root.destroy()
        except tk.TclError:
            pass
        finally:
            self.closed = True

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        header = ttk.Frame(frame)
        header.grid(row=0, column=0, sticky="ew")

        ttk.Label(header, text="Mode").grid(row=0, column=0, sticky="w")
        ttk.Label(header, textvariable=self.mode_value, font=("", 14, "bold")).grid(
            row=1, column=0, sticky="w"
        )

        ttk.Label(header, text="Gesture").grid(row=0, column=1, sticky="w", padx=(24, 0))
        ttk.Label(header, textvariable=self.gesture_value, font=("", 14, "bold")).grid(
            row=1, column=1, sticky="w", padx=(24, 0)
        )

        ttk.Separator(frame).grid(row=1, column=0, sticky="ew", pady=10)

        commands = ttk.Frame(frame)
        commands.grid(row=2, column=0, sticky="ew")

        ttk.Label(commands, text="Gesture").grid(row=0, column=0, sticky="w")
        ttk.Label(commands, text="Command").grid(row=0, column=1, sticky="w", padx=(18, 0))

        for row_index in range(1, 7):
            gesture_label = ttk.Label(commands)
            command_label = ttk.Label(commands)
            gesture_label.grid(row=row_index, column=0, sticky="w", pady=2)
            command_label.grid(row=row_index, column=1, sticky="w", padx=(18, 0), pady=2)
            self.command_rows.append((gesture_label, command_label))

        self._set_commands(MODE_COMMANDS[AppMode.BASE])

    def _set_commands(self, commands: list[tuple[str, str]]) -> None:
        for index, (gesture_label, command_label) in enumerate(self.command_rows):
            if index < len(commands):
                gesture, command = commands[index]
            else:
                gesture, command = "", ""

            gesture_label.configure(text=gesture)
            command_label.configure(text=command)

    def _keep_open(self) -> None:
        self.root.lift()

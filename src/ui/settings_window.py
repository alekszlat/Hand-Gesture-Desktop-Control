"""Startup settings window for editing AppConfig values."""

import tkinter as tk
from tkinter import messagebox, ttk

from config import AppConfig


class SettingsWindow:
    """Tkinter form that returns a validated AppConfig when started."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.result: AppConfig | None = None

        self.root = tk.Tk()
        self.root.title("MBH Settings")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._cancel)

        self.window_name = tk.StringVar(value=config.window_name)
        self.camera_index = tk.StringVar(value=str(config.camera.camera_index))

        self.screen_width = tk.StringVar(value=str(config.cursor.screen_width))
        self.screen_height = tk.StringVar(value=str(config.cursor.screen_height))
        self.cursor_landmark_index = tk.StringVar(
            value=str(config.cursor.cursor_landmark_index)
        )
        self.mouse_update_interval = tk.StringVar(
            value=str(config.cursor.mouse_update_interval)
        )
        self.landmark_smoothing = tk.StringVar(
            value=str(config.cursor.landmark_smoothing)
        )
        self.deadzone_pixels = tk.StringVar(value=str(config.cursor.deadzone_pixels))
        self.loss_hold_seconds = tk.StringVar(
            value=str(config.cursor.loss_hold_seconds)
        )
        self.mirror_x = tk.BooleanVar(value=config.cursor.mirror_x)

        self.gesture_min_confidence = tk.StringVar(
            value=str(config.gesture.min_confidence)
        )
        self.click_cooldown = tk.StringVar(value=str(config.actions.click_cooldown))
        self.launcher_action_cooldown = tk.StringVar(
            value=str(config.actions.launcher_action_cooldown)
        )
        self.window_action_cooldown = tk.StringVar(
            value=str(config.actions.window_action_cooldown)
        )

        self.tracking_model_path = tk.StringVar(value=config.tracking.model_path)
        self.num_hands = tk.StringVar(value=str(config.tracking.num_hands))
        self.min_detection_confidence = tk.StringVar(
            value=str(config.tracking.min_detection_confidence)
        )
        self.min_presence_confidence = tk.StringVar(
            value=str(config.tracking.min_presence_confidence)
        )
        self.min_tracking_confidence = tk.StringVar(
            value=str(config.tracking.min_tracking_confidence)
        )

        self._build()

    def show(self) -> AppConfig | None:
        self.root.mainloop()
        return self.result

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        notebook = ttk.Notebook(frame)
        notebook.grid(row=0, column=0, sticky="nsew")

        self._build_general_tab(notebook)
        self._build_cursor_tab(notebook)
        self._build_tracking_tab(notebook)
        self._build_actions_tab(notebook)

        buttons = ttk.Frame(frame)
        buttons.grid(row=1, column=0, sticky="e", pady=(12, 0))

        ttk.Button(buttons, text="Cancel", command=self._cancel).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(buttons, text="Start", command=self._save).grid(row=0, column=1)

    def _build_general_tab(self, notebook: ttk.Notebook) -> None:
        tab = self._add_tab(notebook, "General")
        self._add_entry(tab, 0, "Window name", self.window_name)
        self._add_entry(tab, 1, "Camera index", self.camera_index)
        self._add_entry(tab, 2, "Gesture min confidence", self.gesture_min_confidence)

    def _build_cursor_tab(self, notebook: ttk.Notebook) -> None:
        tab = self._add_tab(notebook, "Cursor")
        self._add_entry(tab, 0, "Screen width", self.screen_width)
        self._add_entry(tab, 1, "Screen height", self.screen_height)
        self._add_entry(tab, 2, "Cursor landmark index", self.cursor_landmark_index)
        self._add_entry(tab, 3, "Mouse update interval", self.mouse_update_interval)
        self._add_entry(tab, 4, "Landmark smoothing", self.landmark_smoothing)
        self._add_entry(tab, 5, "Deadzone pixels", self.deadzone_pixels)
        self._add_entry(tab, 6, "Loss hold seconds", self.loss_hold_seconds)
        ttk.Checkbutton(tab, text="Mirror X", variable=self.mirror_x).grid(
            row=7, column=1, sticky="w", pady=4
        )

    def _build_tracking_tab(self, notebook: ttk.Notebook) -> None:
        tab = self._add_tab(notebook, "Tracking")
        self._add_entry(tab, 0, "Model path", self.tracking_model_path, width=48)
        self._add_entry(tab, 1, "Number of hands", self.num_hands)
        self._add_entry(tab, 2, "Detection confidence", self.min_detection_confidence)
        self._add_entry(tab, 3, "Presence confidence", self.min_presence_confidence)
        self._add_entry(tab, 4, "Tracking confidence", self.min_tracking_confidence)

    def _build_actions_tab(self, notebook: ttk.Notebook) -> None:
        tab = self._add_tab(notebook, "Actions")
        self._add_entry(tab, 0, "Click cooldown", self.click_cooldown)
        self._add_entry(tab, 1, "Launcher cooldown", self.launcher_action_cooldown)
        self._add_entry(tab, 2, "Window cooldown", self.window_action_cooldown)

    def _add_tab(self, notebook: ttk.Notebook, label: str) -> ttk.Frame:
        tab = ttk.Frame(notebook, padding=12)
        notebook.add(tab, text=label)
        return tab

    def _add_entry(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        variable: tk.StringVar,
        width: int = 18,
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=width).grid(
            row=row, column=1, sticky="ew", pady=4, padx=(12, 0)
        )

    def _save(self) -> None:
        try:
            self._apply_values()
        except ValueError as error:
            messagebox.showerror("Invalid settings", str(error), parent=self.root)
            return

        self.result = self.config
        self.root.destroy()

    def _apply_values(self) -> None:
        self.config.window_name = self._read_text(self.window_name, "Window name")
        self.config.camera.camera_index = self._read_int(
            self.camera_index, "Camera index", minimum=0
        )

        self.config.cursor.screen_width = self._read_int(
            self.screen_width, "Screen width", minimum=1
        )
        self.config.cursor.screen_height = self._read_int(
            self.screen_height, "Screen height", minimum=1
        )
        self.config.cursor.cursor_landmark_index = self._read_int(
            self.cursor_landmark_index, "Cursor landmark index", minimum=0, maximum=20
        )
        self.config.cursor.mouse_update_interval = self._read_float(
            self.mouse_update_interval, "Mouse update interval", minimum=0.0
        )
        self.config.cursor.landmark_smoothing = self._read_float(
            self.landmark_smoothing, "Landmark smoothing", minimum=0.0, maximum=1.0
        )
        self.config.cursor.deadzone_pixels = self._read_int(
            self.deadzone_pixels, "Deadzone pixels", minimum=0
        )
        self.config.cursor.loss_hold_seconds = self._read_float(
            self.loss_hold_seconds, "Loss hold seconds", minimum=0.0
        )
        self.config.cursor.mirror_x = self.mirror_x.get()

        self.config.gesture.min_confidence = self._read_float(
            self.gesture_min_confidence,
            "Gesture min confidence",
            minimum=0.0,
            maximum=1.0,
        )

        self.config.tracking.model_path = self._read_text(
            self.tracking_model_path, "Model path"
        )
        self.config.tracking.num_hands = self._read_int(
            self.num_hands, "Number of hands", minimum=1
        )
        self.config.tracking.min_detection_confidence = self._read_float(
            self.min_detection_confidence,
            "Detection confidence",
            minimum=0.0,
            maximum=1.0,
        )
        self.config.tracking.min_presence_confidence = self._read_float(
            self.min_presence_confidence,
            "Presence confidence",
            minimum=0.0,
            maximum=1.0,
        )
        self.config.tracking.min_tracking_confidence = self._read_float(
            self.min_tracking_confidence,
            "Tracking confidence",
            minimum=0.0,
            maximum=1.0,
        )

        self.config.actions.click_cooldown = self._read_float(
            self.click_cooldown, "Click cooldown", minimum=0.0
        )
        self.config.actions.launcher_action_cooldown = self._read_float(
            self.launcher_action_cooldown, "Launcher cooldown", minimum=0.0
        )
        self.config.actions.window_action_cooldown = self._read_float(
            self.window_action_cooldown, "Window cooldown", minimum=0.0
        )

    def _cancel(self) -> None:
        self.result = None
        self.root.destroy()

    def _read_text(self, variable: tk.StringVar, label: str) -> str:
        value = variable.get().strip()
        if not value:
            raise ValueError(f"{label} cannot be empty.")
        return value

    def _read_int(
        self,
        variable: tk.StringVar,
        label: str,
        minimum: int | None = None,
        maximum: int | None = None,
    ) -> int:
        raw_value = variable.get().strip()
        try:
            value = int(raw_value)
        except ValueError as error:
            raise ValueError(f"{label} must be an integer.") from error

        self._check_range(value, label, minimum, maximum)
        return value

    def _read_float(
        self,
        variable: tk.StringVar,
        label: str,
        minimum: float | None = None,
        maximum: float | None = None,
    ) -> float:
        raw_value = variable.get().strip()
        try:
            value = float(raw_value)
        except ValueError as error:
            raise ValueError(f"{label} must be a number.") from error

        self._check_range(value, label, minimum, maximum)
        return value

    def _check_range(
        self,
        value: int | float,
        label: str,
        minimum: int | float | None,
        maximum: int | float | None,
    ) -> None:
        if minimum is not None and value < minimum:
            raise ValueError(f"{label} must be at least {minimum}.")

        if maximum is not None and value > maximum:
            raise ValueError(f"{label} must be at most {maximum}.")


def open_settings_window(config: AppConfig) -> AppConfig | None:
    return SettingsWindow(config).show()

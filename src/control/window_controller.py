"""Window control backed by xdotool."""

import subprocess
import sys


class WindowController:
    """Controls desktop windows on X11-focused Linux desktops."""

    def close_active_window(self) -> None:
        self._run(["xdotool", "getactivewindow", "windowclose"])

    def close_app(self) -> None:
        sys.exit()

    def minimize_active_window(self) -> None:
        self._run(["xdotool", "getactivewindow", "windowminimize"])

    def activate_window(self, window_id: str | int) -> None:
        self._run(["xdotool", "windowactivate", str(window_id)])

    def get_active_window(self) -> int | None:
        try:
            result = subprocess.check_output(["xdotool", "getactivewindow"], text=True)
            return int(result.strip())
        except (subprocess.CalledProcessError, ValueError):
            return None
        except FileNotFoundError:
            print("xdotool is not installed.")
            return None

    def move_active_window(self, x: int, y: int) -> None:
        self._run(
            [
                "xdotool",
                "getactivewindow",
                "windowmove",
                str(x),
                str(y),
            ]
        )

    def resize_active_window(self, width: int, height: int) -> None:
        self._run(
            [
                "xdotool",
                "getactivewindow",
                "windowsize",
                str(width),
                str(height),
            ]
        )

    def move_window_to_next_monitor(self) -> None:
        """Move the active window to a fixed secondary-monitor position."""
        self.move_active_window(1920, 100)

    def move_window_to_previous_monitor(self) -> None:
        """Move the active window to a fixed primary-monitor position."""
        self.move_active_window(100, 100)

    def _run(self, command: list[str]) -> None:
        try:
            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Window command failed with exit code {e.returncode}: {e.cmd}")
        except FileNotFoundError:
            print("xdotool is not installed.")

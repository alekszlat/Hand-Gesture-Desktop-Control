import subprocess
import sys

class WindowController:
    """
    Controls desktop windows.

    This first version is X11-focused and uses xdotool.
    """

    def close_active_window(self) -> None:
        self._run(["xdotool", "getactivewindow", "windowclose"])

    def close_app(self) -> None:
        #Press Esc to close the app. This is a bit of a hack, but it works for now.
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
        """
        Placeholder version.

        For now this moves the active window to a fixed position
        that you can adjust for your monitor layout.
        """
        self.move_active_window(1920, 100)

    def move_window_to_previous_monitor(self) -> None:
        """
        Placeholder version.

        For now this moves the active window back to the primary screen.
        """
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
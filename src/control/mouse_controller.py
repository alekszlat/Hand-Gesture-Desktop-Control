"""Mouse control backed by xdotool."""

import subprocess


class MouseController:
    """Moves, clicks, and drags the pointer on X11 desktops."""

    def __init__(self):
        self.is_grabbing = False

    def movemouse(self, x, y, sync=False, execute=True):
        command = ["xdotool", "mousemove"]

        if sync:
            command.append("--sync")

        command.extend([str(x), str(y)])

        if execute:
            self._run(command)
        return command

    def mouseclick(self, button=1, sync=False, execute=True):
        command = ["xdotool", "click"]

        if sync:
            command.append("--sync")

        command.append(str(button))

        if execute:
            self._run(command)

        return command

    def mousegrab(self, sync=False, execute=True):
        command = ["xdotool", "mousedown"]
        if sync:
            command.append("--sync")
        command.append("1")
        if execute:
            self._run(command)
        self.is_grabbing = True
        return command

    def mouserelease(self, sync=False, execute=True):
        command = ["xdotool", "mouseup"]
        if sync:
            command.append("--sync")
        command.append("1")
        if execute:
            self._run(command)
        self.is_grabbing = False
        return command

    def _run(self, command: list[str]) -> None:
        try:
            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Mouse command failed with exit code {e.returncode}: {e.cmd}")
        except FileNotFoundError:
            print("xdotool is not installed.")

import subprocess


class AppController:
    """
    Opens desktop applications.
    """

    def __init__(
        self,
        browser_command: str = "firefox",
        vscode_command: str = "code",
        discord_command: str = "discord",
    ):
        self.browser_command = browser_command
        self.vscode_command = vscode_command
        self.discord_command = discord_command

    def open_browser(self) -> None:
        self._launch(self.browser_command)

    def open_vscode(self) -> None:
        self._launch(self.vscode_command)

    def open_discord(self) -> None:
        self._launch(self.discord_command)

    def _launch(self, command: str) -> None:
        try:
            subprocess.Popen(
                command.split(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            print(f"Application command not found: {command}")
        except Exception as e:
            print(f"Failed to launch application '{command}': {e}")
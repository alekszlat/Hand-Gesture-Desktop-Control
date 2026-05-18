from app import App
from config import AppConfig
from ui import open_settings_window

# To do:
# - Better mouse movement smoothing

def main():
    config = open_settings_window(AppConfig())
    if config is None:
        return

    app = App(config=config)
    app.run()


if __name__ == "__main__":
    main()

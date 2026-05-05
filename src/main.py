from app import App

# To do:
# - Better mouse movement smoothing
# - Fix the drag mode (currently very buggy and unreliable)
# - Fix dynamic gesture detection (currently too unreliable)

def main():
    app = App(
        screen_width=1920,
        screen_height=1080,
        cursor_landmark_index=5,
        model_path="models/gesture_recognizer.task",
    )
    app.run()


if __name__ == "__main__":
    main()
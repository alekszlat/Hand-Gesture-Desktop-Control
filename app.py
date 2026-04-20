import CameraStream
import HandTracker
import FrameRenderer
import CursorMapper
import MouseController
import cv2 as cv

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CURSOR_LANDMARK_INDEX = 8
MODEL_PATH = "gesture_recognizer.task"

def main():
    cam = CameraStream.CameraStream()
    hand_tracker = HandTracker.HandTracker(model_path=MODEL_PATH)
    cursor_mapper = CursorMapper.CursorMapper(SCREEN_WIDTH, SCREEN_HEIGHT, CURSOR_LANDMARK_INDEX)
    mouse_controller = MouseController.MouseController()
    frame_renderer = FrameRenderer.FrameRenderer(CURSOR_LANDMARK_INDEX)

    try:
        while True:
            try:
                # Capture frame
                frame = cam.read_frame()

                # Send frame to tracker
                pros_frame = hand_tracker.process_frame(frame)
                latest_result = hand_tracker.get_latest_result()

                # Prepare output image
                output_frame = pros_frame.copy()

                # Map cursor position
                mouse_pos = cursor_mapper.map_to_screen(latest_result)

                if mouse_pos is not None:
                    mouse_controller.movemouse(mouse_pos[0], mouse_pos[1])

                # Draw landmarks and gesture info
                output_frame = frame_renderer.draw_hand_landmarks(output_frame, latest_result)

                cv.imshow("Gesture Detect", output_frame)

                if cv.waitKey(1) & 0xFF == 27:
                    break

            except Exception as e:
                print(f"Error processing frame: {e}")
                break
    finally:
        cam.release()
        hand_tracker.close()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()
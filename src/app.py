import cv2 as cv

from camera import CameraStream
from tracking import HandTracker
from debugging import FrameRenderer

from gestures import (
    CursorMapper,
    GestureInterpreter,
    GestureStateTracker,
    DynamicGestureDetector,
    ModeManager,
)

from control import (
    MouseController,
    AppController,
    WindowController,
    ActionDispatcher,
)


class App:
    def __init__(
        self,
        screen_width=1920,
        screen_height=1080,
        cursor_landmark_index=5,
        model_path="models/gesture_recognizer.task",
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_landmark_index = cursor_landmark_index
        self.model_path = model_path

        self.window_name = "Gesture Detect"
        self.running = False

        # Core input/tracking
        self.cam = CameraStream()
        self.hand_tracker = HandTracker(model_path=self.model_path)

        # Gesture interpretation/state
        self.gesture_interpreter = GestureInterpreter()
        self.gesture_state_tracker = GestureStateTracker()
        self.mode_manager = ModeManager()

        # Cursor and dynamic gestures
        self.cursor_mapper = CursorMapper(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            cursor_landmark_index=self.cursor_landmark_index,
            mirror_x=False,
        )

        self.dynamic_gesture_detector = DynamicGestureDetector(
            landmark_index=self.cursor_landmark_index,
        )

        # Controllers
        self.mouse_controller = MouseController()
        self.app_controller = AppController()
        self.window_controller = WindowController()

        # Dispatcher receives controller instances
        self.action_dispatcher = ActionDispatcher(
            mouse_controller=self.mouse_controller,
            app_controller=self.app_controller,
            window_controller=self.window_controller,
        )

        # Debug renderer
        self.frame_renderer = FrameRenderer(
            cursor_landmark_index=self.cursor_landmark_index
        )

    def run(self):
        self.running = True

        try:
            while self.running:
                self.update()

                if cv.waitKey(1) & 0xFF == 27:
                    self.running = False

        except Exception:
            import traceback
            traceback.print_exc()

        finally:
            self.shutdown()

    def update(self):
        # 1. Read camera frame
        frame = self.cam.read_frame()

        # 2. Send frame to MediaPipe tracker
        processed_frame = self.hand_tracker.process_frame(frame)
        latest_result = self.hand_tracker.get_latest_result()

        # 3. Interpret static gesture
        gesture_name, confidence = self.gesture_interpreter.interpret_gesture(
            latest_result
        )

        # 4. Track gesture state over time
        gesture_state = self.gesture_state_tracker.update(
            gesture_name,
            confidence,
        )

        # 5. Map hand landmark to cursor position
        mouse_pos = self.cursor_mapper.map_to_screen(latest_result)

        # 6. Detect dynamic gestures such as swipes
        dynamic_gesture = self.dynamic_gesture_detector.update(latest_result)

        # 7. Update current app mode
        current_mode = self.mode_manager.update(gesture_state)

        # 8. Dispatch actions
        self.action_dispatcher.dispatch(
            mode=current_mode,
            gesture_state=gesture_state,
            dynamic_gesture=dynamic_gesture,
            cursor_pos=mouse_pos,
        )

        # 9. Render debug output
        output_frame = self.render(
            frame=processed_frame,
            latest_result=latest_result,
            gesture_state=gesture_state,
            current_mode=current_mode,
            dynamic_gesture=dynamic_gesture,
        )

        cv.imshow(self.window_name, output_frame)

    def render(
        self,
        frame,
        latest_result,
        gesture_state,
        current_mode,
        dynamic_gesture,
    ):
        output_frame = frame.copy()

        output_frame = self.frame_renderer.draw_hand_landmarks(
            output_frame,
            latest_result,
        )

        output_frame = self.frame_renderer.draw_gesture_label(
            output_frame,
            gesture_state.name,
        )

        output_frame = self.frame_renderer.draw_mode(
            output_frame,
            current_mode.value,
        )

        # output_frame = self.frame_renderer.draw_dynamic_gesture(
        #     output_frame,
        #     dynamic_gesture,
        # )

        return output_frame

    def shutdown(self):
        self.cam.release()
        self.hand_tracker.close()
        cv.destroyAllWindows()
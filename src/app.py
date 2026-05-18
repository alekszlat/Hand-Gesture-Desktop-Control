"""Application orchestration for camera input, gestures, actions, and UI."""

import cv2 as cv

from camera import CameraStream
from config import AppConfig
from tracking import HandTracker
from debugging import FrameRenderer

from gestures import (
    CursorMapper,
    GestureInterpreter,
    GestureStateTracker,
    ModeManager,
)

from control import (
    MouseController,
    AppController,
    WindowController,
    ActionDispatcher,
)
from ui import StatusWidget


class App:
    """Owns the main realtime loop and connects the app subsystems."""

    def __init__(self, config: AppConfig | None = None):
        self.config = config or AppConfig()
        self.window_name = self.config.window_name
        self.running = False

        self.cam = CameraStream(camera_index=self.config.camera.camera_index)
        self.hand_tracker = HandTracker(
            model_path=self.config.tracking.model_path,
            num_hands=self.config.tracking.num_hands,
            min_detection_confidence=self.config.tracking.min_detection_confidence,
            min_presence_confidence=self.config.tracking.min_presence_confidence,
            min_tracking_confidence=self.config.tracking.min_tracking_confidence,
        )

        self.gesture_interpreter = GestureInterpreter(
            min_confidence=self.config.gesture.min_confidence
        )
        self.gesture_state_tracker = GestureStateTracker()
        self.mode_manager = ModeManager()

        self.cursor_mapper = CursorMapper(
            screen_width=self.config.cursor.screen_width,
            screen_height=self.config.cursor.screen_height,
            cursor_landmark_index=self.config.cursor.cursor_landmark_index,
            mouse_update_interval=self.config.cursor.mouse_update_interval,
            mirror_x=self.config.cursor.mirror_x,
            landmark_smoothing=self.config.cursor.landmark_smoothing,
            deadzone_pixels=self.config.cursor.deadzone_pixels,
            loss_hold_seconds=self.config.cursor.loss_hold_seconds,
        )

        self.mouse_controller = MouseController()
        self.app_controller = AppController()
        self.window_controller = WindowController()

        self.action_dispatcher = ActionDispatcher(
            mouse_controller=self.mouse_controller,
            app_controller=self.app_controller,
            window_controller=self.window_controller,
            click_cooldown=self.config.actions.click_cooldown,
            launcher_action_cooldown=self.config.actions.launcher_action_cooldown,
            window_action_cooldown=self.config.actions.window_action_cooldown,
        )

        self.frame_renderer = FrameRenderer(
            cursor_landmark_index=self.config.cursor.cursor_landmark_index
        )
        self.status_widget = (
            StatusWidget() if self.config.ui.show_status_widget else None
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
        frame = self.cam.read_frame()

        processed_frame = self.hand_tracker.process_frame(frame)
        latest_result = self.hand_tracker.get_latest_result()

        gesture_name, confidence = self.gesture_interpreter.interpret_gesture(
            latest_result
        )

        gesture_state = self.gesture_state_tracker.update(
            gesture_name,
            confidence,
        )

        mouse_pos = self.cursor_mapper.map_to_screen(latest_result)

        current_mode = self.mode_manager.update(gesture_state)

        if self.status_widget is not None:
            self.status_widget.update(
                mode=current_mode,
                gesture_name=gesture_state.name,
            )

        self.action_dispatcher.dispatch(
            mode=current_mode,
            gesture_state=gesture_state,
            cursor_pos=mouse_pos,
        )

        output_frame = self.render(
            frame=processed_frame,
            latest_result=latest_result,
            gesture_state=gesture_state,
            current_mode=current_mode,
        )

        cv.imshow(self.window_name, output_frame)

    def render(
        self,
        frame,
        latest_result,
        gesture_state,
        current_mode,
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

        return output_frame

    def shutdown(self):
        if self.status_widget is not None:
            self.status_widget.destroy()

        self.cam.release()
        self.hand_tracker.close()
        cv.destroyAllWindows()

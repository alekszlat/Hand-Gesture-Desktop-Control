import cv2 as cv

class CameraStream:
    def __init__(self, camera_index=0):
        self.cap = cv.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open camera with index {camera_index}")

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Unable to read frame from camera")
        return frame

    def release(self):
        self.cap.release()
import cv2 as cv
import numpy as np

def detect_faces(img, cascade):
    """Detect faces in an image using Haar Cascade."""
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=4,
        minSize=(30, 30),
        flags=cv.CASCADE_SCALE_IMAGE
    )
    
    return faces

def draw_faces(img, faces):
    """Draw rectangles around detected faces."""
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv.putText(img, f'Faces: {len(faces)}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def main():
    # Load cascade classifier
    cascade = cv.CascadeClassifier(
        cv.samples.findFile('haarcascade_frontalface_alt.xml')
    )

    # Open camera
    cam = cv.VideoCapture(0)

    while True:
        ret, img = cam.read()
        if not ret:
            break
        
        faces = detect_faces(img, cascade)
        draw_faces(img, faces)

        cv.imshow('facedetect', img)

        if cv.waitKey(5) == 27:  # ESC key
            break

    cam.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()

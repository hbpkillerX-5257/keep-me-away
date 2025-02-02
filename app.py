import cv2
import numpy as np
import time
import tkinter as tk
import argparse
from collections import deque

class ScreenProtector:
    def __init__(self, threshold_factor=1.2, calibration_time=2, buffer_size=30, fps=15):
        self.threshold_factor = threshold_factor
        self.calibration_time = calibration_time
        self.buffer_size = buffer_size
        self.fps = fps
        
        # Face detection model
        self.net = cv2.dnn.readNetFromCaffe(
            "deploy.prototxt",
            "res10_300x300_ssd_iter_140000.caffemodel"
        )
        
        # Screen blanking window
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.blank_label = tk.Label(self.root, bg='black')
        self.blank_label.pack(expand=True, fill=tk.BOTH)
        self.root.withdraw()
        
        self.cap = cv2.VideoCapture(0)
        self.baseline_area = None
        self.alert_active = False
        self.alert_start_time = 0
        self.area_buffer = deque(maxlen=buffer_size)

    def calibrate(self):
        print("Calibrating... Stay at your normal distance from the screen")
        start_time = time.time()
        areas = []
        
        while time.time() - start_time < self.calibration_time:
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            area = self.detect_face_area(frame)
            if area:
                areas.append(area)
                
            cv2.imshow("Calibration", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        if areas:
            self.baseline_area = np.mean(areas)
            print(f"Calibration complete. Baseline area: {self.baseline_area:.2f}")
        else:
            raise Exception("No face detected during calibration")
        
        cv2.destroyWindow("Calibration")

    def detect_face_area(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0)
        )
        
        self.net.setInput(blob)
        detections = self.net.forward()
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                return (endX - startX) * (endY - startY)
        
        return None

    def run(self):
        self.calibrate()
        threshold_area = self.baseline_area * self.threshold_factor
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            current_area = self.detect_face_area(frame)
            self.area_buffer.append(current_area if current_area else 0)
            
            if current_area and current_area > threshold_area:
                if not self.alert_active:
                    self.alert_start_time = time.time()
                    self.alert_active = True
                    print("Too close! Move back!")
                
                elapsed = time.time() - self.alert_start_time
                if elapsed >= 5:
                    self.root.deiconify()
                    self.root.update()
                else:
                    cv2.putText(frame, f"Too close! {5 - int(elapsed)}s", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                if self.alert_active:
                    self.root.withdraw()
                    self.alert_active = False
            
            avg_area = np.mean([a for a in self.area_buffer if a])
            cv2.putText(frame, f"Area: {avg_area:.2f} / {threshold_area:.2f}", 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Screen Protector", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=1.2,
                        help="Threshold factor multiplier for baseline area")
    args = parser.parse_args()

    protector = ScreenProtector(threshold_factor=args.threshold)
    protector.run()
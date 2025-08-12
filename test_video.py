import cv2
from Source.LaneDetector import LaneDetector
from Source.Utils import get_video_resolution
import time, sys

filepath = r"Resources/videos/test2.mp4"
if len(sys.argv) > 1:
    filepath = sys.argv[1]
cap = cv2.VideoCapture(filepath)
LD = LaneDetector("pipeline.json", controls=True, controls_resolution=(650, 785))
#LD.setup_record(get_video_resolution(cap), output_path=f'{filepath.split(".")[0]}_output.avi', record_fps=60)

while cap.isOpened():
    start = time.time()
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    output_frame = LD.frame_processor(frame, frame_skip=5)
    end = time.time()
    totalTime = end - start
    fps = 1 / totalTime if totalTime > 0 else 0

    cv2.putText(output_frame, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Lane Detection", output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        LD.stop_recording()
        break

cap.release()
cv2.destroyAllWindows()
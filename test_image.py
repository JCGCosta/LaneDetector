import cv2
import sys
from Source.LaneDetector import LaneDetector

if __name__ == "__main__":
    filepath = r"Resources/images/lane.jpg"
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    image = cv2.imread(filepath)
    LD = LaneDetector(pipeline="pipeline.json", controls=True, controls_resolution=(700, 800))
    while True:
        output_image = LD.frame_processor(image, alpha=1.0, beta=0.5)
        cv2.imshow("Lane Detector", output_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(f"{filepath.split('.')[0]}_output.jpg", output_image)
            break
    cv2.destroyAllWindows()
import cv2
from Source.LaneDetector import LaneDetector

if __name__ == "__main__":
    filepath = r"Resources/images/lane.jpg"
    image = cv2.imread(filepath)
    LD = LaneDetector(pipeline="pipeline.json", controls=False)
    output_image = LD.frame_processor(image, alpha=1.0, beta=0.5)
    cv2.imshow("Lane Detector", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
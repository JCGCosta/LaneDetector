import cv2
from Source.LaneDetector import LaneDetector

if __name__ == "__main__":
    filepath = r"Resources/images/lane1.jpg"
    image = cv2.imread(filepath)
    LD = LaneDetector(pipeline="pipeline.json", controls=True)
    while True:
        output_image = LD.frame_processor(image, alpha=1.0, beta=0.5)
        cv2.imshow("Lane Detector", output_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(f"{filepath.split('.')[0]}_output.jpg", output_image)
            break
    cv2.destroyAllWindows()
# LaneDetection

> This repository show a Lane Detection pipeline part of a Lane Departure Warning System, through the implementation of a computer vision pipeline strategy to detect lane lines in roads.
The real gain is that the algorithm parameters can be calibrated on the fly, making it possible to do fine-tuning, and map supervised different image/video datasets.

## Installation and Running:

### Step 1: Prerequisites

- Make sure you have Python installed on your system. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).
- Also make sure you have git installed in your machine. You can download git here: https://git-scm.com/downloads


### Step 2: Clone this repository

- Open your terminal or command prompt and navigate to the directory where you want to clone this repository. Then run the following command:

```bash
# Navigate to the directory where you want to create your project
git clone https://github.com/JCGCosta/LaneDetector.git
```

### Step 3: Creating a Virtual Environment

```bash
# Navigate to the directory where you cloned the repository
cd repository/directory/path

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment (If you are on Windows)
.\venv\Scripts\activate

# Activate the virtual environment (If you are on Linux)
source venv/bin/activate

# Now inside the environment install the libraries from the requirements.txt
pip install -r requirements.txt
```

### Step 4: Configuration Files

- To make your own image processing pipeline you must edit the `pipeline_sample.py` file, which must follow the schema.

```json
{
  "Operation": {
    "path": "path/to/your/file.py",
    "function": "function name to be called",
    "parameters": {
      "parameter1": [
        127, # The initial Value of the parameter
        255  # The maximum value of the parameter, which can be changed by the user
      ],...
    }
  },...
}
```

- The operations are executed in order, and will receive the image as cv2.Mat of size (width, height, 3) and the parameters defined in the pipeline file, if you are confused about it take a look in the Source/ImageProcessing folder, where there is some examples.

### Step 5: Testing Samples

- Before running make sure you have the `pipeline_sample.json` file configured with the correct path of your python file from your computer.
- As a sample the ImageProcessing folder inside Source already have a full pipeline with 5 operations for the Lane Detection.
- **ATTENTION**: Also, please change in the three testing.py files the `pipeline.json` to `pipeline_sample.json` in the LaneDetector class instantiation, so it will use your pipeline file.

### Step 6: Running the Application
- To run the application, you can choose between three options:
  - Run the `test_image.py` file with a image file path as the first argument directly, which will run the pipeline with the default parameters.
  - Run the `test_video.py` file with a video file path as the first argument, which will run the pipeline on the video.
  - Run the `test_camera.py` file, which will run the pipeline on the camera video.

```bash
# Navigate to the main directory
cd repository/directory/path

# Run the test_image.py with an image file path
python test_image.py path/to/your/image.jpg

# Run the test_video.py with a video file path
python test_video.py path/to/your/video.mp4

# Run the test_camera.py to run the pipeline on the camera video
python test_camera.py
```

### Step 7: Building with the Lane Detection Object

- To build the Lane Detection Object, you can learn by exploring the testing.py files.

```python
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
```

### Step 3: Results

https://github.com/JCGCosta/RealTimeCalibrationLaneDetection/assets/51680369/e55424ea-66c4-4918-8cbe-a3c2f7244c2f

© Julio César Guimarães Costa 2023. All rights reserved.

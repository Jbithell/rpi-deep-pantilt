# Raspberry Pi Lecture Tracking

# Build List

  - [Raspberry Pi 4 - 4GB minimum](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
  - [Raspberry Pi Camera - V2 minimum](https://www.raspberrypi.org/products/camera-module-v2/)
  - Micro SD card 16+ GB
  - Micro HDMI Cable
  - [12" CSI/DSI ribbon for Raspberry Pi Camera](https://www.adafruit.com/product/1648) (optional, but highly recommended)
  
# Installation

1. [Install Raspbian](https://www.raspberrypi.org)

1. Change Password

1. Run `sudo raspi-config` and select `Interfacing Options` from the Raspberry Pi Software Configuration Tool’s main menu. Press ENTER.

1. Select the Enable Camera option and enable the use of the Camera

1. Select the SSH option and enable the use of remote SSH

1. `sudo apt update && sudo apt upgrade -y && sudo apt auto-remove -y`

1. `sudo apt install -y cmake python3-dev libjpeg-dev libatlas-base-dev raspi-gpio libhdf5-dev python3-smbus`

1. `python3 -m venv .venv`

1. `source .venv/bin/activate`

1. `pip install --upgrade setuptools`

1. `git clone https://github.com/Jbithell/rpi-lectureTrack`

1. `cd rpi-lectureTrack`

1. `pip install tensorflow-2.2.0-cp37-cp37m-linux_armv7l.whl`

1. `pip install click picamera pillow smbus`

1. `python setup.py install`

## Testing Detection

The `detect` command will start a PiCamera preview and render detected objects as an overlay. Verify you're able to detect an object before trying to track it. 

`rpi-lectureTrack detect person`

```
rpi-lectureTrack detect --help
Usage: rpi-lectureTrack detect [OPTIONS] [LABELS]...

  rpi-lectureTrack detect [OPTIONS] [LABELS]

    LABELS (optional)     One or more labels to detect, for example:     
    $ rpi-lectureTrack detect person book "wine glass"

    If no labels are specified, model will detect all labels in this list:
    $ rpi-lectureTrack list-labels

    Detect command will automatically load the appropriate model

    For example, providing "face" as the only label will initalize
    FaceSSD_MobileNet_V2 model $ rpi-lectureTrack detect face

    Other labels use SSDMobileNetV3 with COCO labels $ rpi-lectureTrack detect
    person "wine class" orange

Options:
  --loglevel TEXT  Run object detection without pan-tilt controls. Pass
                   --loglevel=DEBUG to inspect FPS.
  --edge-tpu       Accelerate inferences using Coral USB Edge TPU
  --rotation INTEGER  PiCamera rotation. If you followed this guide, a
                      rotation value of 0 is correct.
                      https://medium.com/@grepLeigh/real-time-object-tracking-
                      with-tensorflow-raspberry-pi-and-pan-tilt-
                      hat-2aeaef47e134
  --help           Show this message and exit.

```

## Lecturer Tracking with Zones Output

The following will start a PiCamera preview, render detected objects as an overlay, and track an object's movement whilst sending it out to Crestron

`rpi-lectureTrack track`

```
Usage: rpi-lectureTrack track [OPTIONS] [LABEL]

  rpi-lectureTrack track [OPTIONS] [LABEL]

  LABEL (required, default: person) Exactly one label to detect, for example:     
  $ rpi-lectureTrack track person

  Track command will automatically load the appropriate model

  For example, providing "face" will initalize FaceSSD_MobileNet_V2 model
  $ rpi-lectureTrack track face

  Other labels use SSDMobileNetV3 model with COCO labels 
  $ rpi-lectureTrack detect orange

Options:
  --loglevel TEXT  Pass --loglevel=DEBUG to inspect FPS and tracking centroid
                   X/Y coordinates
  --edge-tpu       Accelerate inferences using Coral USB Edge TPU
  --rotation INTEGER  PiCamera rotation. If you followed this guide, a
                      rotation value of 0 is correct.
                      https://medium.com/@grepLeigh/real-time-object-tracking-
                      with-tensorflow-raspberry-pi-and-pan-tilt-
                      hat-2aeaef47e134
  --help           Show this message and exit.
```

## Valid labels for Object Detection/Tracking

`rpi-lectureTrack list-labels`

The following labels are valid tracking targets.

```
['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
```

## Object Detection & Tracking

### `FLOAT32` model (`ssd_mobilenet_v3_small_coco_2019_08_14`)

`rpi-lectureTrack detect` and `rpi-lectureTrack track` perform inferences using this model. Bounding box and class predictions render at roughly *6 FPS* on a *Raspberry Pi 4*.  

The model is derived from  `ssd_mobilenet_v3_small_coco_2019_08_14` in [tensorflow/models](https://github.com/tensorflow/models). I extended the model with an NMS post-processing layer, then converted to a format compatible with TensorFlow 2.x (FlatBuffer). 

I scripted the conversion steps in `tools/tflite-postprocess-ops-float.sh`. 

## Credits

The MobileNetV3-SSD model in this package was derived from [TensorFlow's model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md), with [post-processing ops added](https://gist.github.com/leigh-johnson/155264e343402c761c03bc0640074d8c).

The PID control scheme in this package was inspired by [Adrian Rosebrock](https://github.com/jrosebr1) tutorial [Pan/tilt face tracking with a Raspberry Pi and OpenCV](https://www.pyimagesearch.com/2019/04/01/pan-tilt-face-tracking-with-a-raspberry-pi-and-opencv/)

The original package [rpi-lectureTrack](https://github.com/leigh-johnson/rpi-lectureTrack) by Leigh Johnson and was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.

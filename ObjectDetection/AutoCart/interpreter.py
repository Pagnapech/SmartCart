# Path for Working Directories

# Import library
import os
import argparse
from threading import Thread
import importlib.util

##### This  uses to parse the data to be more readable
def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('--modeldir', help='Folder the .tflite file is located in', required=True)
    parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite', default='detect.tflite')
    parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt', default='labelmap.txt')
    parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects', default=0.5)
    parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.', default='1280x720')
    parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection', action='store_true')
    
    return parser

def setupInterpreter():
    
    parser = parsing() 
    # Retrieve the data from Parser Argument 
    args = parser.parse_args()
    
    MODEL_NAME = args.modeldir  # Correct directory name

    GRAPH_NAME = args.graph
    LABELMAP_NAME = args.labels
    min_conf_threshold = float(args.threshold) #set as float
    resW , resH = args.resolution.split('x')
    imW , imH = int(resW), int(resH) #set as integer
    use_TPU = args.edgetpu
    
    # Import TensorFlow libraries
    # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
    # If using Coral Edge TPU, import the load_delegate library
    
    # Find the specs of the imported library
    pkg = importlib.util.find_spec('tflite_runtime')
    
    if(pkg):
        from tflite_runtime.interpreter import Interpreter
        if (use_TPU):
            from tflite_runtime.interpreter import load_delegate
    
    else:
        from tensorflow.lite.python.interpreter import Interpreter
        if (use_TPU):
            from tflite_runtime.interpreter import load_delegate
    
    # If using Edge TPU, assign filename for Edge TPU model
    if (use_TPU):
        # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
        if (GRAPH_NAME == 'detect.tflite'):
            GRAPH_NAME = 'edgetpu.tflite' 
    
    # Get path to current working directionary
    CWD_PATH = os.getcwd()
    
#     # Path to video file
#     VIDEO_PATH = os.path.join(CWD_PATH,VIDEO_NAME)

    # Path to .tflite file, which contains the model that is used for object detection
    PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)
    
    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)
    
    # Load the label map
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    
    # COCO starter model from '???'
    # remove it
    if labels[0] == '???':
        del(labels[0])
    
    # Load TensorFlow Lite model
    # If using Edge TPU, use special load_delegate argument
    if (use_TPU):
        interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                  experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        print(PATH_TO_CKPT)
    else:
        interpreter = Interpreter(model_path=PATH_TO_CKPT)
    
    return interpreter, imW, imH, min_conf_threshold, labels 

        
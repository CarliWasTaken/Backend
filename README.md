# Carli Backend
This is the Backend for Carli. The Backend is deployed on the RaspberryPi or Jetson Nano that sits on the car. 


## Installation
First, install the requirements with pip:
```bash
pip install -r requirements.txt
```

Then run it on the device with python:
```bash
python server.py
```

## Server
The entrypoint is `server.py`. This creates a UDP Socket.
### Structure
 The messages that come frome the frontend have the following structure:
```
{
  "steer": x, 
  "speed": y
}
```
X and Y are numbers between -1 and 1. 
- 0 would be center for the steering and parked for the speed
- 1 would be right for the steering and full speed forwards for the speed
- -1 would be left for the steering and full speed backwards for the speed

`server.py` decodes these messages and processes them.

### How it works
The class `Server` is a singleton class and has the methods `start` and `stop`. They respectively start and stop the server. It also has the method `receive_data`, which takes the next `_bufferSize` of Bytes and converts it to JSON data. It is important that the Buffer Size be the same on the Frontend and Backend.

The server runs in an infinite loop. The rate at which it receives packages is controlled by the frontend. It first collects the data and then checks whether it is valid. If it is valid, it will process the data. If it is not, it will stop the car.

There is also a special case for the AI Mode. This is when the speed value is exactly 123. Then it will ignore both the steering and speed values and query the neural network for the steering angle. The speed for the AI Mode is constant. Note that this speed may have to be tuned while the car is being driven, because with different battery levels the speed varies.

The server can also be configured in a number of ways. The IP can be set with `_localIP`. If it should be reachable over the network, it is important that this ip not be localhost. The port can also be changed to one's desire with the `_localPort` variable. The buffer size can be changed with the `_bufferSize` variable.

Whether training data should be collected or not can be configured with the boolean `_collect_training_data`. If set to true, it will take a picture after a number of messages, defined by `_collect_training_data_freq`, are received. This picture with the corresponding steering angle is then saved. The steering angle is contained in the filename with a timestamp. The frequency is necessary because the RaspberryPi is overwhelmed if it has to take and save a picture every time it receives a message. It would lead to unsmooth handling of the vehicle.

## Modules
There are four modules:
- car
- cam
- nn
- log

Each of these fulfills a seperate task and work indepently from each other, which means that they can be abstracted.

### Car Module
The `Controller` class in `controller.py` is a singleton class and it takes the values from -1 to 1 and translates them into hardware values which will be used by the `AgentMoveController`, implemented in `agent.py` which sends the corresponding PWM Signals to control the motors. The server can call either the `steer`, `drive` or `stop` function, all of which do exactly what the name suggests.

`AgentMoveController` is also implemented in `dev_agent.py`. This class is different in that it doesn't do anything with the values. With this class, the program can be tested without needing to use the car itself.

The `_max_throttle_increment` in `Controller` is the biggest value that the throttle can be incremented by in one method call. The frontend sends messages 60 times a second, which means that with a value of 0.01, max speed is reached in 1.67 seconds. This is needed because the motors seem to have difficutly handling instantaneous speed changes.

The car module also provides the `Safety` class in `safety.py`. This is a singleton class which is used in `server.py`. Every time a message is received, the safety class is updated by the server. When there haven't been any messages for a certain amount of time (0.5 seconds), it stops the vehicle to prevent it from going out of control.

### Cam Module
The `Camera` class in `camera.py` is a singleton class and provides methods for capturing the current image of the camera. If the parameter `process_frame` is True (default is True), then it also processes the frame to be used by the Neural Network.

`camera_server.py` also provides a seperate flask server which can be used to transmit a live video feed. This is currently WIP.

### NN Module
The `CustomNeuralNetwork` class in `custom_neural_network.py` is a self-made neural network trained on collected training data. It currently doesn't work because of performance constraints. If this project is continued it is probably best to process the imagery on a seperate machine as the RaspberryPi is very weak and can't use modern machine learning librariers like TensorFlow of PyTorch because it has a 32bit CPU.

### Log Module
The provides the `Log` class in `log.py`. It simply provides a uniform interface for logging and it also saves these logs. The common logging levels like info, debug, error and more are included.

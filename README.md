# Carli Backend
This is the Backend for Carli. The Backend is deployed on the RaspberryPi or Jetson Nano that sits on the car. Run it on the device simply via:
```
python3 server.py
```

## Structure
The entrypoint is `server.py`. This creates a UDP Socket which listens on `20001`. The messages that come frome the frontend have the following structure:
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

`server.py` decodes these messages and sends the commands to `controls.py` for further processing. It also provides an emergency stop.

`controls.py` takes the values from -1 to 1 and translates them into Hardware Values, which can then be used by `agent.py`. It also doesn't allow very big changes with the speed, as this could cause issues.

The `max_throttle_increment` is the biggest value that the throttle can be incremented by in one method call. The frontend sends messages 60 times a second, which means that with a value of 0.01, max speed is reached in 1.67 seconds.

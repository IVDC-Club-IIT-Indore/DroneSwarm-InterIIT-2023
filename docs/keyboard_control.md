### Control Pluto Drone using keyboard <br>
To control the drone flight interactively using the following keyboard keymap call the keyboard_control() function from the ```main.py```
```python3
drone.keyboard_control()
```

          w                                                      ↑
     a    s    d                                            ←    ↓    → 
    
    spacebar       : arm / disarm
    w              : increase throttle
    s              : decrease throttle
    q              : take off
    e              : land
    a              : turn left  (negative yaw)
    d              : turn right (positive yaw)
    p              : flip
    Up arrow(↑)    : go forward     (positive pitch)
    Down arrow(↓)  : go backward  (negative pitch)
    Left arrow(←)  : go left
    Right arrow(→) : go right
    CTRL+C to quit

Note: The Drone Movement is with respect to user's [frame of reference](https://en.wikipedia.org/wiki/Frame_of_reference).

import keyboard
from gpiozero import Motor  ,DistanceSensor
from time import sleep
import csv
from datetime import datetime

front_left_motor = Motor(forward=12, backward=17)
front_right_motor = Motor(forward=18, backward=27)
back_left_motor = Motor(forward=22, backward=23)
back_right_motor = Motor(forward=24, backward=25)


frontSensor = DistanceSensor(echo=19, trigger=13)
backSensor = DistanceSensor(echo=20, trigger=16)

#Motor
def stop():
    front_left_motor.stop()
    front_right_motor.stop()
    back_left_motor.stop()
    back_right_motor.stop()

def move_forward(speed=1):
    front_left_motor.forward(speed)
    front_right_motor.forward(speed)
    back_left_motor.forward(speed)
    back_right_motor.forward(speed)

def move_backward(speed=1):
    front_left_motor.backward(speed)
    front_right_motor.backward(speed)
    back_left_motor.backward(speed)
    back_right_motor.backward(speed)

def move_left(speed=1):
    front_left_motor.backward(speed)
    front_right_motor.forward(speed)
    back_left_motor.forward(speed)
    back_right_motor.backward(speed)

def move_right(speed=1):
    front_left_motor.forward(speed)
    front_right_motor.backward(speed)
    back_left_motor.backward(speed)
    back_right_motor.forward(speed)

def rotate_clockwise(speed=1):
    front_left_motor.forward(speed)
    front_right_motor.backward(speed)
    back_left_motor.forward(speed)
    back_right_motor.backward(speed)

def rotate_counterclockwise(speed=1):
    front_left_motor.backward(speed)
    front_right_motor.forward(speed)
    back_left_motor.backward(speed)
    back_right_motor.forward(speed)

def move_forward_left(speed=1):
    front_left_motor.stop()
    front_right_motor.forward(speed)
    back_left_motor.forward(speed)
    back_right_motor.stop()

def move_forward_right(speed=1):
    front_left_motor.forward(speed)
    front_right_motor.stop()
    back_left_motor.stop()
    back_right_motor.forward(speed)

def move_backward_left(speed=1):
    front_left_motor.stop()
    front_right_motor.backward(speed)
    back_left_motor.backward(speed)
    back_right_motor.stop()

def pivot_front_right(speed=1):
    front_left_motor.forward(speed)
    front_right_motor.backward(speed)
    back_left_motor.stop() 
    back_right_motor.stop()

def pivot_front_left(speed=1):
    front_left_motor.backward(speed)
    front_right_motor.forward(speed)
    back_left_motor.stop() 
    back_right_motor.stop()

def pivot_back_right(speed=1):
    front_left_motor.stop() 
    front_right_motor.stop() 
    back_left_motor.backward(speed)
    back_right_motor.forward(speed)

def pivot_back_left(speed=1):
    front_left_motor.stop() 
    front_right_motor.stop() 
    back_left_motor.forward(speed)
    back_right_motor.backward(speed)

def pivot_right_forward(speed=1):
    front_left_motor.stop() 
    front_right_motor.forward(speed)
    back_left_motor.stop() 
    back_right_motor.forward(speed)

def pivot_right_backward(speed=1):
    front_left_motor.stop() 
    front_right_motor.backward(speed)
    back_left_motor.stop() 
    back_right_motor.backward(speed)

def pivot_left_forward(speed=1):
    front_left_motor.forward(speed)
    front_right_motor.stop() 
    back_left_motor.forward(speed)
    back_right_motor.stop() 

def pivot_left_backward(speed=1):
    front_left_motor.backward(speed)
    front_right_motor.stop() 
    back_left_motor.backward(speed)
    back_right_motor.stop() 



def log_distances(front, back, to_file=False):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{timestamp} | Front: {front:.1f} cm | Back: {back:.1f} cm"
    print(log_line)
    
    if to_file:
        with open("distance_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, front, back])


def auto_drive():
    print("Autonomous mode started. Press CTRL+C to stop.")
    try:
        while True:
            front = frontSensor.distance * 100  # in cm
            back = backSensor.distance * 100    # in cm

            print(f"Front: {front:.1f} cm | Back: {back:.1f} cm")
            log_distances(front, back, to_file=True)
            
            if front > 40:
                move_forward()
            else:
                stop()
                print("Obstacle ahead. Deciding direction...")

                # Try turning right slightly and measure
                rotate_clockwise()
                sleep(0.5)
                stop()
                sleep(0.2)
                right_check = frontSensor.distance * 100
                print(f"Right side distance: {right_check:.1f} cm")

                # Turn back to center
                rotate_counterclockwise()
                sleep(0.5)
                stop()
                sleep(0.2)

                # Try turning left slightly and measure
                rotate_counterclockwise()
                sleep(0.5)
                stop()
                sleep(0.2)
                left_check = frontSensor.distance * 100
                print(f"Left side distance: {left_check:.1f} cm")

                # Return to center
                rotate_clockwise()
                sleep(0.5)
                stop()
                sleep(0.2)

                # Decide direction
                if left_check > right_check and left_check > 30:
                    print("Turning left...")
                    rotate_counterclockwise()
                    sleep(0.6)
                    stop()
                elif right_check > left_check and right_check > 30:
                    print("Turning right...")
                    rotate_clockwise()
                    sleep(0.6)
                    stop()
                elif back > 30:
                    print("Backing up...")
                    move_backward()
                    sleep(1)
                    stop()
                    rotate_clockwise()
                    sleep(0.6)
                    stop()
                else:
                    print("Surrounded! Stopping.")
                    stop()
                    sleep(1)

            sleep(0.1)

    except KeyboardInterrupt:
        stop()
        print("Autonomous mode stopped.")


def control_robot():
    print("Use keys to control the robot:")
    print("""
        Z - Forward
        S - Backward
        Q - Left
        D - Right
        A - Rotate Counterclockwise
        E - Rotate Clockwise
        R - Diagonal Forward Left
        T - Diagonal Forward Right
        F - Diagonal Backward Left
        G - Diagonal Backward Right
        U - Pivot Front Left
        I - Pivot Front Right
        J - Pivot Back Left
        K - Pivot Back Right
        O - Pivot Left Forward
        L - Pivot Left Backward
        P - Pivot Right Forward
        M - Pivot Right Backward
        Space - Stop
        ESC - Exit
    """)
    
    while True:
        if keyboard.is_pressed('z'):
            move_forward()
        elif keyboard.is_pressed('s'):
            move_backward()
        elif keyboard.is_pressed('q'):
            move_left()
        elif keyboard.is_pressed('d'):
            move_right()
        elif keyboard.is_pressed('a'):
            rotate_counterclockwise()
        elif keyboard.is_pressed('e'):
            rotate_clockwise()
        elif keyboard.is_pressed('r'):
            move_forward_left()
        elif keyboard.is_pressed('t'):
            move_forward_right()
        elif keyboard.is_pressed('f'):
            move_backward_left()
        elif keyboard.is_pressed('g'):
            move_backward_right()
        elif keyboard.is_pressed('u'):
            pivot_front_right()
        elif keyboard.is_pressed('i'):
            pivot_front_left()
        elif keyboard.is_pressed('j'):
            pivot_back_right()
        elif keyboard.is_pressed('k'):
            pivot_back_left()
        elif keyboard.is_pressed('o'):
            pivot_right_forward()
        elif keyboard.is_pressed('l'):
            pivot_right_backward()
        elif keyboard.is_pressed('p'):
            pivot_left_forward()
        elif keyboard.is_pressed('m'):
            pivot_left_backward()
        elif keyboard.is_pressed('space'):
            stop()
        elif keyboard.is_pressed('esc'):
            stop()
            print("Exiting...")
            break
        else:
            stop()

        front = frontSensor.distance * 100
        back = backSensor.distance * 100
        log_distances(front, back)

        sleep(0.05)

if __name__ == "__main__":
    mode = input("Enter 'a' for auto mode or 'm' for manual mode: ").strip().lower()
    if mode == 'a':
        auto_drive()
    else:
        try:
            control_robot()
        except KeyboardInterrupt:
            stop()

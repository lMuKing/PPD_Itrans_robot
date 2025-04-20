from gpiozero import DistanceSensor
from time import sleep

frontSensor = DistanceSensor(echo=19, trigger=13)
backSensor = DistanceSensor(echo=20, trigger=16)

try:
    print("Testing Front and Back Distance Sensors (CTRL+C to stop)...")
    while True:
        front = frontSensor.distance * 100  # in cm
        back = backSensor.distance * 100   # in cm
        print(f"Front Distance: {front:.1f} cm | Back Distance: {back:.1f} cm")
        sleep(0.3)
except KeyboardInterrupt:
    print("\nStopped by user.")

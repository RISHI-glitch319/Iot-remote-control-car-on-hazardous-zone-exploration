import RPi.GPIO as GPIO
from time import sleep

# Motor driver pins for the 12V DC motor (forward/backward)
in1 = 21
in2 = 20

# Motor driver pins for the 6V DC motor (right/left)
in3 = 24
in4 = 23

# Enable pins for motor speed control (PWM)
en1 = 25  # PWM pin for 12V motor speed control
en2 = 12  # PWM pin for 6V motor speed control

# Variable to track the direction of the 12V motor (forward or backward)
temp1 = 1

# Set up the GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)

# Set initial state of all motors to stop
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

# Initialize PWM for speed control
pwm1 = GPIO.PWM(en1, 1000)  # PWM for the 12V motor
pwm2 = GPIO.PWM(en2, 1000)  # PWM for the 6V motor

pwm1.start(25)  # Start with 25% duty cycle (low speed) for 12V motor
pwm2.start(25)  # Start with 25% duty cycle (low speed) for 6V motor

print("\n")
print("The default speed & direction of motors is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high a-Left d-right e-exit")
print("\n")

# Main control loop
while True:
    x = input()  # Changed to input() for Python 3 compatibility

    if x == 'r':
        print("run")
        if temp1 == 1:
            GPIO.output(in1, GPIO.HIGH)  # Forward for 12V motor
            GPIO.output(in2, GPIO.LOW)
            print("forward")
        else:
            GPIO.output(in1, GPIO.LOW)  # Backward for 12V motor
            GPIO.output(in2, GPIO.HIGH)
            print("backward")

    elif x == 's':
        print("stop")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

    elif x == 'f':
        print("forward")
        GPIO.output(in1, GPIO.HIGH)  # Forward for 12V motor
        GPIO.output(in2, GPIO.LOW)
        temp1 = 1  # Set direction to forward for the 12V motor

    elif x == 'b':
        print("backward")
        GPIO.output(in1, GPIO.LOW)  # Backward for 12V motor
        GPIO.output(in2, GPIO.HIGH)
        temp1 = 0  # Set direction to backward for the 12V motor

    elif x == 'a':
        print("Left")
        GPIO.output(in3, GPIO.LOW)  # Left for 6V motor
        GPIO.output(in4, GPIO.HIGH)

    elif x == 'd':
        print("Right")
        GPIO.output(in3, GPIO.HIGH)  # Right for 6V motor
        GPIO.output(in4, GPIO.LOW)

    elif x == 'l':
        print("low")
        pwm1.ChangeDutyCycle(25)  # Set speed to low for 12V motor
        pwm2.ChangeDutyCycle(25)  # Set speed to low for 6V motor
    elif x == 'm':
        print("medium")
        pwm1.ChangeDutyCycle(50)  # Set speed to medium for 12V motor
        pwm2.ChangeDutyCycle(50)  # Set speed to medium for 6V motor
    elif x == 'h':
        print("high")
        pwm1.ChangeDutyCycle(75)  # Set speed to high for 12V motor
        pwm2.ChangeDutyCycle(75)  # Set speed to high for 6V motor

    elif x == 'e':
        print("Exiting...")
        GPIO.cleanup()  # Clean up GPIO pins when exiting
        break

    else:
        print("<<<  Wrong data  >>>")
        print("Please enter the defined data to continue.....")

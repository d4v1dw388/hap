import time
import RPi.GPIO as GPIO

import os.path
import rrdtool

# Filename (absolute path)
rrd_file = '/home/pi/hap-deployed/boiler.rrd'

# Logging interval in seconds
interval = 5

# Check File
if not os.path.isfile(rrd_file):
    # Create RRD tool database
    rrdtool.create(
        rrd_file,
        '--step',  str(interval),  # interval
        '--start', 'N',  # start now
        'DS:burner:GAUGE:2000:U:U',
        'DS:circulation_pump:GAUGE:2000:U:U',
        'DS:charge_pump:GAUGE:2000:U:U',
        'RRA:AVERAGE:0.5:1:120960'  # last week without average
    )

# Use RPi.GPIO layout
GPIO.setmode(GPIO.BOARD)

# Pin 11 to 13 (GPIO 17 to 19) as input
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Loop
while 1:
    # Read GPIO
    burner      = (GPIO.input(11) == GPIO.LOW)
    circulation = (GPIO.input(12) == GPIO.LOW)
    charge      = (GPIO.input(13) == GPIO.LOW)

    if burner:
        print('B'),
    else:
        print('b'),

    if circulation:
        print('C'),
    else:
        print('c'),

    if charge:
        print('W')
    else:
        print('w')

    rrdtool.update(rrd_file, 'N:%d:%d:%d' % (burner, circulation, charge))

    # Wait for 5 seconds
    time.sleep(interval)


import time
import RPi.GPIO as GPIO

import os.path
import rrdtool

# generate PNG
# while true; do rrdtool graph '/var/www/heating.png' -s 'N-2400' -w 1020 -h 300 'DEF:burner=heating.rrd:burner:AVERAGE' 'DEF:circulation=heating.rrd:circulation:AVERAGE' 'DEF:charge=heating.rrd:charge:AVERAGE' 'LINE2:burner#ff0000' 'AREA:circulation#009900' 'AREA:charge#0000DD80'; sleep 60; done

# Filename
rrd_file = 'heating.rrd'

# Check File
if not os.path.isfile(rrd_file):
  # Create RRD tool database
  rrdtool.create(
    rrd_file, 
    '--step',  '5', # interval
    '--start', 'N', # start now
    'DS:burner:GAUGE:2000:U:U',
    'DS:circulation:GAUGE:2000:U:U',
    'DS:charge:GAUGE:2000:U:U',
    'RRA:AVERAGE:0.5:1:120960') # last week without average

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 11 (GPIO 17) auf Input setzen
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Dauersschleife
while 1:
  # GPIO lesen
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

  # Warte 5 Sekunden
  time.sleep(5)


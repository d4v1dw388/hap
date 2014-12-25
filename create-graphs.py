import rrdtool
import time

rrd_file_boiler = '/home/pi/hap-deployed/boiler.rrd'
png_file_boiler = '/var/www/boiler.png'

rrd_file_temperatures = 'heating-temperatures.rrd'
png_file_temperatures = '/var/www/heating-temperatures.png'

while True:
    # Boiler
    rrdtool.graph(
        png_file_boiler,
        '-s N-21600',
        '-w 1000',
        '-h  400',
        '--vertical-label', 'State',
        'DEF:burner=%s:burner:AVERAGE' % (rrd_file_boiler,),
        'DEF:circulation=heating.rrd:circulation:AVERAGE',
        'DEF:charge=heating.rrd:charge:AVERAGE',
        'AREA:circulation#88ff88',
        'AREA:charge#0000ff88',
        'LINE2:burner#ff0000')

    # Temperatures
    rrdtool.graph(
        png_file_temperatures,
        '-s N-28800',
        '-w 1000',
        '-h  400',
        '--title=Buderus',
        '--rigid',
        '--vertical-label', 'Degree Celsius',
        '--y-grid=5:1',
        'DEF:feed=heating-temperatures.rrd:feed:LAST',
        'DEF:return=heating-temperatures.rrd:return:LAST',
        'DEF:burner=heating.rrd:burner:AVERAGE',
        'CDEF:burner_scale=burner,100,*',
        'AREA:burner_scale#ffdddd:Burner         ',
        'GPRINT:burner_scale:LAST:Current\:%8.2lf%% %s',
        'GPRINT:burner_scale:AVERAGE:Average\:%7.2lf%% %s\\n',
        'LINE2:feed#ff0000:Flow  ',
        'GPRINT:feed:LAST:Current\:%8.2lf %s',
        'GPRINT:feed:AVERAGE:Average\:%8.2lf %s',
        'GPRINT:feed:MAX:Maximum\:%8.2lf %s',
        'GPRINT:feed:MIN:Minimum\:%8.2lf %s\\n',
        'LINE2:return#0000bb:Return ',
        'GPRINT:return:LAST:Current\:%8.2lf %s',
        'GPRINT:return:AVERAGE:Average\:%8.2lf %s',
        'GPRINT:return:MAX:Maximum\:%8.2lf %s',
        'GPRINT:return:MIN:Minimum\:%8.2lf %s\\n')
    # break

    print('Done.')
    time.sleep(5)

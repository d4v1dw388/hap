import rrdtool

rrd_file_boiler = '/home/pi/hap-deployed/boiler.rrd'
png_file_boiler = '/var/www/boiler'

rrd_file_temperatures = 'heating-temperatures.rrd'
png_file_temperatures = '/var/www/heating-temperatures.png'


class CreateGraphs:
    def __init__(self):
        pass

    def graph(self):
        # Boiler
        # 10m
        # 1h
        # 8h
        # 24h
        # 3d
        # 7d
        times = [
            10 * 60,
            60 * 60,
            8 * 60 * 60,
            24 * 60 * 60,
            3 * 24 * 60 * 60,
            7 * 24 * 60 * 60]

        for t in times:
            rrdtool.graph(
                png_file_boiler + str(t) + '.png',
                '-s N-%s' % (t,),
                '-w 800',
                '-h 350',
                '-m 2',
                '--vertical-label', 'State',

                'DEF:burner=%s:burner:AVERAGE' % (rrd_file_boiler,),
                'DEF:circulation=%s:circulation_pump:AVERAGE' % (rrd_file_boiler,),
                'DEF:charge=%s:charge_pump:AVERAGE' % (rrd_file_boiler,),

                'CDEF:burner_scale=burner,100,*',
                'CDEF:circulation_scale=circulation,100,*',
                'CDEF:charge_scale=charge,100,*',

                'AREA:circulation_scale#88ff88:Circulation Pump',
                'GPRINT:circulation_scale:LAST:Current\:%8.2lf%% %s',
                'GPRINT:circulation_scale:AVERAGE:Average\:%7.2lf%% %s\\n',

                'AREA:charge_scale#0000ff88:Charge Pump     ',
                'GPRINT:charge_scale:LAST:Current\:%8.2lf%% %s',
                'GPRINT:charge_scale:AVERAGE:Average\:%7.2lf%% %s\\n',

                'LINE2:burner_scale#ff0000:Burner          ',
                'AREA:burner_scale#ff000040',
                'GPRINT:burner_scale:LAST:Current\:%8.2lf%% %s',
                'GPRINT:burner_scale:AVERAGE:Average\:%7.2lf%% %s\\n',
            )

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

if __name__ == '__main__':
    print('Testing Create Graphs')
    cg = CreateGraphs()
    cg.graph()

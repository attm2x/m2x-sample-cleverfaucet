import time
import glob


class OneWireTempSensor(object):
    base_dir = '/sys/bus/w1/devices/'  # only on pi
    test_dir = 'tests/devices/'
    temperature_file = '/w1_slave'

    # Default to Raspberry Pi device directory
    # One wire sensors each have unique serial number of the form 28-xxxx
    # represented as string
    def __init__(self, serial, base_dir='/sys/bus/w1/devices/'):
        self.base_dir = base_dir
        self.serial = serial
        self.device_file = self.base_dir + self.serial + '/w1_slave'
        self.tempc = None
        self.tempf = None

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            self.tempc = float(temp_string) / 1000.0
            self.tempf = self.tempc * 9.0 / 5.0 + 32.0

    def get_tempc(self):
        return self.tempc

    def get_tempf(self):
        return self.tempf

    @classmethod
    def find_temp_sensors(cls, testing=False):
        """
        Need to make sure modprobe w1-gpio and modprobe w1-therm modules
        are running 
        """
        if testing:
            device_folders = glob.glob(cls.test_dir + '28*')
        else:
            device_folders = glob.glob(cls.base_dir + '28*')
        device_numbers = []
        for folder in device_folders:
            number = folder[folder.rfind('/')+1:]
            device_numbers.append(number)

        return device_numbers


class FlowMeter(object):
    SECONDS_IN_A_MINUTE = 60
    MS_IN_A_SECOND = 1000.0
    MIN_HZ = 0.25  # Minimum rate of clicks, in Hz, that we are willing to count as an actual flow
    MAX_HZ = 80  # Maximum rate of clicks, in Hz, that we are willing to count as an actual flow

    def __init__(self, temp_sensor=None):
        self.temp_sensor = temp_sensor  # Should be name of OneWireTempSensor object
        self.clicks = 0
        self.lastClick = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        self.clickDelta = 0  # ms
        self.hertz = 0.0  # Hz
        self.flow = 0.0  # L/s
        self.thisFlow = 0.0  # L
        self.totalFlow = 0.0  # L
        self.enabled = True

    def update(self, currentTime):
        self.clicks += 1
        # get time delta
        self.clickDelta = max((currentTime - self.lastClick), 1)
        if self.enabled and self.clickDelta < 1000:
            self.hertz = FlowMeter.MS_IN_A_SECOND / self.clickDelta
            if FlowMeter.MIN_HZ < self.hertz < FlowMeter.MAX_HZ:
                self.flow = self.hertz / (FlowMeter.SECONDS_IN_A_MINUTE * 7.5)
                instFlow = self.flow * (self.clickDelta / FlowMeter.MS_IN_A_SECOND)
                self.thisFlow += instFlow
                self.totalFlow += instFlow
        self.lastClick = currentTime

    def checkTempC(self):
        if self.temp_sensor is not None:
            self.temp_sensor.read_temp()
            return self.temp_sensor.get_tempc()
        return None

    def checkTempF(self):
        if self.temp_sensor is not None:
            self.temp_sensor.read_temp()
            return self.temp_sensor.get_tempf()
        return None

    def getFormattedClickDelta(self):
        return str(self.clickDelta) + ' ms'

    def getFormattedHertz(self):
        return str(round(self.hertz, 3)) + ' Hz'

    def getFormattedFlow(self):
        return str(round(self.flow, 3)) + ' L/s'

    def getFormattedThisFlow(self):
        return str(round(self.thisFlow, 3)) + ' L'

    def getThisFlow(self):
        return round(self.thisFlow, 3)

    def getFormattedTotalFlow(self):
        return str(round(self.totalFlow, 3)) + ' L'

    def getTotalFlow(self):
        return round(self.totalFlow, 3)

    def clear(self):
        self.thisFlow = 0
        self.totalFlow = 0

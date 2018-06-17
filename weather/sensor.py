#!/usr/bin/python

import sys
from time import sleep, strftime
from OmegaExpansion import onionI2C # requires fixes for https://github.com/OnionIoT/i2c-exp-driver/issues/13
import io
import os

while True:
    # Init
    i2c     = onionI2C.OnionI2C()

    # temp / humidity sensor (0x40)
    i2c.write(0x40, [0xE5])
    sleep(0.1)
    h0, h1 = i2c.read(0x40, 2)

    i2c.write(0x40, [0xE0])
    sleep(0.1)
    t0, t1 = i2c.read(0x40, 2)

    hum = ((125.0 * (h0 * 256 + h1)) / 65536.0) - 6.0
    temp = ((175.72 * (t0 * 256 + t1)) / 65536.0) - 46.85;

    # light sensor (0x39)
    
    i2c.writeByte(0x39, 0x00 | 0x80, 0x0B)
    # TSL2571 address, 0x39(57)
    # Select ALS time register, 0x01(01) with command register, 0x80(128)
    #		0xFF(255)	Atime = 2.72 ms, Max count = 1023
    i2c.writeByte(0x39, 0x01 | 0x80, 0xFF)
    # TSL2571 address, 0x39(57)
    # Select wait time register, 0x03(03) with command register, 0x80(128)
    #		0xFF(255)	Wtime = 2.72 ms
    i2c.writeByte(0x39, 0x03 | 0x80, 0xFF)
    # TSL2571 address, 0x39(57)
    # Select control register, 0x0F(15) with command register, 0x80(128)
    #		0x20(32)	Gain = 1x
    i2c.writeByte(0x39, 0x0F | 0x80, 0x20)

    sleep(0.5)

    # TSL2571 address, 0x39(57)
    # Read data back from 0x14(20) with command register, 0x80(128), 4 bytes
    # c0Data LSB, c0Data MSB, c1Data LSB, c1Data MSB
    data = i2c.readBytes(0x39, 0x14 | 0x80, 4)

    # Convert the data
    c0Data = data[1] * 256 + data[0]
    c1Data = data[3] * 256 + data[2]
    CPL = (2.72 * 1.0) / 53.0;
    luminance1 = (1 * c0Data - 2.0 * c1Data) / CPL
    luminance2 = (0.6 * c0Data - 1.00 * c1Data) / CPL
    luminance = 0.0
    if luminance1 > 0 and luminance2 > 0 :
      if luminance1 > luminance2 :
        luminance = luminance1
      else :
        luminance = luminance2

    # print '%s | RH: %0.1f %% | Temp: %0.1f C | Ambient Light Luminance: %.2f lux' % (
    #     strftime('%X'),
    #     hum,
    #     temp,
    #     luminance
    # )

    json_data_wget = '{"value1": %0.1f, "value2": %0.1f, "value3": %.2f}' % (hum, temp, luminance)
    json_data_status = '{"RH": "%0.1f %%", "temp": "%0.1f C", "ALL": "%.2f lux"}' % (hum, temp, luminance)
    # print json_data
    file = open('/www/status.json', 'w')
    file.write(json_data_status)
    file.close()
    command = 'wget -O /dev/null --post-data=\''+json_data_wget+'\' --header=Content-Type:application/json "https://maker.ifttt.com/trigger/weather_sensor_reading/with/key/g47mO9YQUHSaSldhZdvS5iEnSRM4BIii4yK672IkuI0"'
    # print command

    # subprocess.Popen(
    #   'which wget'
    # )

    # subprocess.Popen(
    #   command
    # )

    # subprocess.check_output(['bash','-c', command])

    os.system(command)

    sleep(60 * 5)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
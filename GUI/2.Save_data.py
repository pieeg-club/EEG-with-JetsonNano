import pandas as pd
import spidev
import time
import Jetson.GPIO as GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)

from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy import signal

input_drdy = 7
GPIO.setup(input_drdy, GPIO.IN, pull_up_down=GPIO.PUD_UP)

from time import sleep
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=100000

#spi.max_speed_hz=25000
spi.lsbfirst=False
#spi.cshigh=False
#spi.cslow=True

spi.mode=0b01
spi.bits_per_word = 8

who_i_am=0x00
config1=0x01
config2=0X02
config3=0X03

reset=0x06
stop=0x0A
start=0x08
sdatac=0x11
rdatac=0x10
wakeup=0x02
rdata = 0x12

ch1set=0x05
ch2set=0x06
ch3set=0x07
ch4set=0x08
ch5set=0x09
ch6set=0x0A
ch7set=0x0B
ch8set=0x0C

data_test= 0x7FFFFF
data_check=0xFFFFFF

def read_byte(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 read_reg=spi.xfer(data)
 print ("data", read_reg)
 
def send_command(command):
# GPIO.output(18, False)
 send_data = [command]
 com_reg=spi.xfer(send_data)
# GPIO.output(18, True)
 
def write_byte(register,data):
# GPIO.output(18, False)
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)
 spi.xfer(data)
# GPIO.output(18, True)

send_command (wakeup)
send_command (stop)
send_command (reset)
send_command (sdatac)

#write_byte (0x14, 0x80) #GPIO
write_byte (config1, 0x96)
write_byte (config2, 0xD4)
write_byte (config3, 0xFF)
write_byte (0x04, 0x00)
write_byte (0x0D, 0x00)
write_byte (0x0E, 0x00)
write_byte (0x0F, 0x00)
write_byte (0x10, 0x00)
write_byte (0x11, 0x00)
write_byte (0x15, 0x20)
#
write_byte (0x17, 0x00)
write_byte (ch1set, 0x00)
write_byte (ch2set, 0x00)
write_byte (ch3set, 0x00)
write_byte (ch4set, 0x00)
write_byte (ch5set, 0x00)
write_byte (ch6set, 0x00)
write_byte (ch7set, 0x00)
write_byte (ch8set, 0x00)

send_command (rdatac)
send_command (start)
DRDY=1

result=[0]*27
data_1ch_test = []
data_2ch_test = []
data_3ch_test = []
data_4ch_test = []
data_5ch_test = []
data_6ch_test = []
data_7ch_test = []
data_8ch_test = []

figure, axis = plt.subplots(8, 1)
plt.subplots_adjust(hspace=1) 

axis_x=0
y_minus_graph=250
y_plus_graph=250
x_minux_graph=5000
x_plus_graph=250
sample_len = 250

axi = [0,1,2,3,4,5,6,7]
for ax in axi:
    axis[ax].set_xlabel('Time')
    axis[ax].set_ylabel('Amplitude')
    axis[ax].set_title('Data after pass filter')
test_DRDY = 5 

#1.2 Band-pass filter
data_before = []
data_after =  []
just_one_time = 0

sample_len = 250
sample_lens = 250
fps = 250
highcut = 1
lowcut = 10
#data_before_1 = data_before_2 = data_before_3 = data_before_4 = data_before_5 = data_before_6 = data_before_7 = data_before_8 = [0]*250

while 1:
    button_state = GPIO.input(input_drdy)
    if button_state == 1:
        test_DRDY = 10
    if test_DRDY == 10 and button_state == 0:
        test_DRDY = 0 

        output=spi.readbytes(27)
        for a in range (3,25,3):
            voltage_1=(output[a]<<8)| output[a+1]
            voltage_1=(voltage_1<<8)| output[a+2]
            convert_voktage=voltage_1|data_test
            if convert_voktage==data_check:
                voltage_1_after_convert=(voltage_1-16777214)
            else:
                voltage_1_after_convert=voltage_1
            channel_num =  (a/3)
            result[int (channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)
           #a print (channel_num, result[int (channel_num)])
        data_1ch_test.append(result[1])

        data_2ch_test.append(result[2])

        data_3ch_test.append(result[3])
        data_4ch_test.append(result[4])
        data_5ch_test.append(result[5])
        data_6ch_test.append(result[6])
        data_7ch_test.append(result[7])
        data_8ch_test.append(result[8])


        if len(data_1ch_test)==10000:

            
            data_dict = {
                'data_1ch_test': data_1ch_test,
                'data_2ch_test': data_2ch_test,
                'data_3ch_test': data_3ch_test,
                'data_4ch_test': data_4ch_test,
                'data_5ch_test': data_5ch_test,
                'data_6ch_test': data_6ch_test,
                'data_7ch_test': data_7ch_test,
                'data_8ch_test': data_8ch_test
                        }

# Convert dictionary to DataFrame

            df = pd.DataFrame(data_dict)
            df.to_excel("1ch_test.xlsx", index=False)  # Change "output.xlsx" to your desired file name
            import sys
            print (df)
            sys.exit()
spi.close()

import ctypes
import time
libc = ctypes.CDLL("./super_real_time.so")

libc.prepare()

while 1: 
 print (libc.real())


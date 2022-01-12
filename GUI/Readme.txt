
For SPI 
From
https://github.com/vsergeev/c-periphery
to receive dynamic library - libperiphery.a
$ mkdir build
$ cd build
$ cmake ..
$ make

to receive static library
gcc -fpic -shared -home/Desktop/new_spi/c-periphery-master/src super_real_time_massive.c /home/Desktop/new_spi/c-periphery-master/build/libperiphery.a -o super_real_time_massive.so




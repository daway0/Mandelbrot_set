#
#
# THIS IS DIRTY, DONT TOUCH IT
#
#
from PIL import Image, ImageDraw
import cmath
import sys
import threading


class c_thread(threading.Thread):
    def __init__(self, x_start, x_end, height):
        super(c_thread, self).__init__()
        self.__height = height
        self.__x_start = x_start
        self.__x_end = x_end
        self.__data = []

    def run(self):
        self.__draw_man(self.__x_start, self.__x_end)

    def get_data(self):
        return self.__data

    def __draw_man(self, x_start, x_end):  # img object
        for x in range(x_start, x_end):
            for y in range(self.__height):

                z = complex((realc_left+(x/width)*lenc_),
                            (imgc_down+(y/self.__height)*lenc_))
                c = self.__man_check(z)
                self.__data.append((x, y, self.__get_color(c)))

    def __man_check(self, z):
        #
        #  C IS THE KERNEL 
        #   FOR MANDELBROT USE c=z 
        #   FOR OTHER , USE c = complex(-0.8, 0.3) AND PLAY WITH NUMBERS
        counter = 1
        #c = z
        c = complex(-0.9, 0.3)
        while abs(z) <= 2 and counter <= 255:
            z = z*z + c
            counter += 1
        return counter

    def __get_color(self, it):
        if it < 63:

            return(int(0 + it / 63 * 32), int(7 + it / 63 *
                                              100), int(100 + it / 63 * 103), 1)

        elif it >= 63 and it < 127:

            return(int(32 + (it - 63) / 63 * 205), int(107 + (it - 63) /
                                                       63 * 148), int(203 + (it - 63) / 63 * 52), 1)

        elif it >= 127 and it < 191:

            return(int(237 + (it - 127) / 63 * 18), int(255 - (it - 127) /
                                                        63 * 85), int(255 - (it - 127) / 63 * 255), 1)

        else:

            return(int(255 - (it - 191) / 63 * 255),
                   int(170 - (it - 191) / 63 * 168), 0, 1)


sys.stdout = open('1th.txt', 'w')


# 1 1000 11s
# 2      11.175s
# 4      12.133s
# 8      11.164s
height = 2500
width = 2500
img = Image.new('RGB', (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

realc_left = -2
realc_right = 2
imgc_up = 2
imgc_down = -2
lenc_ = 4


'''img2 = Image.new('RGB', (256, 10))
draw2 = ImageDraw.Draw(img2)

for x in range(256):
    for y in range(10):
        draw2.point((x, y), get_color(x))

img2.show()
img2.save('pallet.png')'''

count = 8
th_list = []
for i in range(count):
    chunck = int(width/count)
    thread = c_thread(chunck * i, chunck*(i+1), height)
    th_list.append(thread)
    thread.start()


# draw_man(draw, 0, width)
for i in range(count):
    th_list[i].join()


for i in range(count):
    data = th_list[i].get_data()
    for x, y, color in data:
        draw.point((x, y), (color[0],color[1],color[2]))

img.show()
img.save('first5.png')

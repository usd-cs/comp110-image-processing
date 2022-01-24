"""
Module: comp110_image

Module that allows for basic 2D image manipulation.

Author: Sat Garcia (sat@sandiego.edu)
"""

from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def is_valid_color_value(val):
    """ Returns true if val is within the valid range for a color component (0
    to 255) and false otherwise. """
    return isinstance(val, int) and (0 <= val <= 255)

def validate_rgb_list(color):
    """ Checks that given value (color) is a list with 3 valid RGB values,
    throwing an exception of it is not. """
    if not isinstance(color, list):
        raise TypeError("color must be given as an RGB list.")

    elif len(color) != 3:
        raise ValueError("color list must be in format [r, g, b]")

    elif not (is_valid_color_value(color[0]) \
                and is_valid_color_value(color[1]) \
                and is_valid_color_value(color[2])):

        raise ValueError(f"RGB values ({color}) must be int values between 0 and 255")


class Pixel:
    """A class to represent a single pixel in an image."""

    def __init__(self, color=None):
        if color is None:
            # if color isn't specified, make a black pixel
            self.color = [0, 0, 0]
        else:
            validate_rgb_list(color)
            self.__color = color

    def copy(self):
        """Returns a copy of this Pixel object."""
        return Pixel(self.color)

    @property
    def color(self):
        """Returns color of pixel as an [r, g, b] list."""
        return self.__color[:]

    @color.setter
    def color(self, new_color):
        """
        Changes color of this Pixel.
        """
        validate_rgb_list(new_color)
        self.red = new_color[0]
        self.green = new_color[1]
        self.blue = new_color[2]

    @property
    def red(self):
        """Returns red component of pixel."""
        return self.__color[0]

    @red.setter
    def red(self, new_red):
        """Changes value of red component."""
        if not is_valid_color_value(new_red):
            raise ValueError(f"red value ({new_red}) must be an int between 0 and 255")
        else:
            self.__color[0] = new_red

    @property
    def green(self):
        """Returns green component of pixel."""
        return self.__color[1]

    @green.setter
    def green(self, new_green):
        """Changes value of green component."""
        if not isinstance(new_green, int):
            raise ValueError(f"green value ({new_green}) must be an int between 0 and 255")
        else:
            self.__color[1] = new_green

    @property
    def blue(self):
        """Returns blue component of pixel."""
        return self.__color[2]

    @blue.setter
    def blue(self, new_blue):
        """Changes value of blue component."""
        if not isinstance(new_blue, int):
            raise ValueError(f"blue value ({new_blue}) must be an int between 0 and 255")
        else:
            self.__color[2] = new_blue



    def __str__(self):
        return "Pixel with red=%d, green=%d, blue=%d" % (self.red, self.green,
                                                         self.blue)

    def __eq__(self, other):
        """
        Checks for equality of this pixel and another one.

        Two pixels are considered equal if their colors are the same.
        """
        return self.red == other.red \
                and self.green == other.green \
                and self.blue == other.blue


    def __ne__(self, other):
        return not self == other


# Definitions of common colors
Black = Pixel([0, 0, 0])
White = Pixel([255, 255, 255])
Gray = Pixel([128, 128, 128])
Red = Pixel([255, 0, 0])
Lime = Pixel([0, 255, 0])
Blue = Pixel([0, 0, 255])
Yellow = Pixel([255, 255, 0])
Cyan = Pixel([0, 255, 255])
Magenta = Pixel([255, 0, 255])
Silver = Pixel([192, 192, 192])
Maroon = Pixel([128, 0, 0])
Green = Pixel([0, 128, 0])
Navy = Pixel([0, 0, 128])
Lavender = Pixel([230, 230, 250])


class Picture:
    """This class represents a digital picture/image."""

    def __init__(self, width=100, height=100, title=None, pic=None, filename=None):

        if pic is not None:
            # If we were given an existing pic, then create a copy of that
            self.__width = pic.get_width()
            self.__height = pic.get_height()
            self.__title = pic.get_title()

            self.__data = [[pic.get_pixel(x, y).color
                            for x in range(self.__width)]
                                for y in range(self.__height)]


        elif filename is not None:
            # If we are given a filename, then open that file and read in
            image = Image.open(filename)
            self.__width = image.width
            self.__height = image.height
            self.__title = title

            def get_image_rgb(img, x, y):
                """Returns Pixel with color of pixel at (x,y) in given image."""
                if img.mode == "RGB":
                    color = list(img.getpixel((x,y)))
                elif img.mode == "L":
                    # luminence is grayscale... given as a single value
                    l = img.getpixel((x,y))
                    color = [l, l, l]
                else:
                    print(img.mode)
                    raise RuntimeError("Image in %s has unsupported mode: %s" %
                            (filename, img.mode))

                return color

            self.__data = [[get_image_rgb(image, x, y)
                            for x in range(self.__width)]
                                for y in range(self.__height)]


        else:
            # If we weren't given an existing pic, create a new blank one of the
            # specified width and height.
            self.__width = width
            self.__height = height
            self.__title = title
            self.__data = [[[0, 0, 0] for x in range(width)] for y in range(height)]

        self.__pixels = [[Pixel(self.__data[y][x])
                            for x in range(self.__width)]
                                for y in range(self.__height)]

    def copy(self):
        """Returns a copy of this Pixel object."""
        return Picture(pic=self)

    def get_pixel(self, x, y):
        """Returns Pixel object at the specified (x,y) coordinates."""
        return self.__pixels[y][x]

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        self.__title = new_title

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def show(self):
        """Displays the picture in a new window."""

        ax = plt.imshow(self.__data)
        plt.tick_params(axis='x', bottom=False, top=True, labelbottom=False,
                        labeltop=True)
        plt.show()


    def save(self, filename):
        """ Saves this picture to a file with the given file name. """
        img = Image.new('RGB', (self.__width, self.__height), 255)
        data = img.load()

        for x in range(self.__width):
            for y in range(self.__height):
                data[x,y] = self.get_pixel(x,y).color

        img.save(filename)

    def __str__(self):
        return "A picture with width = %d and height = %d" % (self.width, self.height)

    def __eq__(self, other):
        """
        Checks for equality of this Picture and another one.

        Two Pictures are considered equal if the colors of all their pixels are
        the same. The title of the pictures may differ between equal Picture
        objects though.
        """
        if self.width != other.width or self.height != other.height:
            return False

        # check all individual pixels for equality
        for x in range(self.width):
            for y in range(self.height):
                if self.get_pixel(x,y) != other.get_pixel(x,y):
                    return False

        return True

    def __ne__(self, other):
        """
        Checks for inequality of this Picture and another one.

        Two Pictures are considered equal if the colors of all their pixels are
        the same. The title of the pictures may differ between equal Picture
        objects though.
        """
        return not self == other


    def __iter__(self):
        """Return new iterator for pixels in this Picture."""
        self.__iterx = 0
        self.__itery = 0
        return self

    def __next__(self):
        """Returns the next pixel for iteration."""

        if self.__iterx != (self.__width - 1):
            # move one column to the right if we can
            self.__iterx += 1
            return self.__pixels[self.__itery][self.__iterx]
        elif self.__itery != (self.__height - 1):
            # reached right edge, move down a row if we can
            self.__iterx = 0
            self.__itery += 1
            return self.__pixels[self.__itery][self.__iterx]
        else:
            # reached last pixel: we DONE!
            raise StopIteration


if __name__ == "__main__":
    pic = Picture(256, 512)
    pic.title = "Color Gradient"

    # create color gradient in picture
    for x in range(pic.width):
        for y in range(pic.height):
            pix = pic.get_pixel(x,y)
            pix.color = [x % 256, y % 256, (x+y) % 256]

    pic.show()

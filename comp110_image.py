"""
Module: comp110_image

Module that allows for basic 2D image manipulation.

Author: Sat Garcia (sat@sandiego.edu)
"""

from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class Color:
    """ A class to represent an RGB color. """

    def __init__(self, r, g, b):
        # check that all components are in valid range
        Color.check_rgb_value_range(r)
        Color.check_rgb_value_range(g)
        Color.check_rgb_value_range(b)

        self.__red = int(r)
        self.__green = int(g)
        self.__blue = int(b)

    def copy(self):
        """Returns a copy of this Color object."""
        return Color(self.__red, self.__green, self.__blue)

    def check_rgb_value_range(val):
        """Checks if given value is within the valid range for an RGB
        component."""
        if val < 0 or val > 255:
            raise ValueError("Value must be between 0 and 255.")


    def get_red(self):
        """Returns red component of color."""
        return self.__red

    def get_green(self):
        """Returns green component of color."""
        return self.__green

    def get_blue(self):
        """Returns blue component of color."""
        return self.__blue

    def get_rgb(self):
        """Returns red, green, and blue components as a tuple."""
        return (self.__red, self.__green, self.__blue)

    def get_average(self):
        """Returns the average value of color components."""
        return (self.__red + self.__green + self.__blue) // 3

    def set_rgb(self, new_rgb):
        """Changes red, green, and blue components to given values."""
        Color.check_rgb_value_range(new_rgb[0])
        Color.check_rgb_value_range(new_rgb[1])
        Color.check_rgb_value_range(new_rgb[2])
        self.__red = int(new_rgb[0])
        self.__green = int(new_rgb[1])
        self.__blue = int(new_rgb[2])

    def set_red(self, new_red):
        """Changes value of red component."""
        Color.check_rgb_value_range(new_red)
        self.__red = int(new_red)

    def set_green(self, new_green):
        """Changes value of green component."""
        Color.check_rgb_value_range(new_green)
        self.__green = int(new_green)

    def set_blue(self, new_blue):
        """Changes value of blue component."""
        Color.check_rgb_value_range(new_blue)
        self.__blue = int(new_blue)

    def __str__(self):
        return "Color: red = %d, green = %d, blue = %d" % (self.__red,
                self.__green, self.__blue)

    def __eq__(self, other):
        return self.__red == other.get_red() \
                and self.__green == other.get_green() \
                and self.__blue == other.get_blue()

    def __ne__(self, other):
        return self.__red != other.get_red() \
                or self.__green != other.get_green() \
                or self.__blue != other.get_blue()


    # camelCase alternative naves
    getRGB = get_rgb
    getRed = get_red
    getGreen = get_green
    getBlue = get_blue
    getAverage = get_average
    setRGB = set_rgb
    setRed = set_red
    setGreen = set_green
    setBlue = set_blue


# Definitions of common colors
Black = Color(0, 0, 0)
White = Color(255, 255, 255)
Gray = Color(128, 128, 128)
Red = Color(255, 0, 0)
Lime = Color(0, 255, 0)
Blue = Color(0, 0, 255)
Yellow = Color(255, 255, 0)
Cyan = Color(0, 255, 255)
Magenta = Color(255, 0, 255)
Silver = Color(192, 192, 192)
Maroon = Color(128, 0, 0)
Green = Color(0, 128, 0)
Navy = Color(0, 0, 128)
Lavender = Color(230, 230, 250)


class Pixel:
    """A class to represent a single pixel in an image."""

    def __init__(self, color=None, x=0, y=0):
        self.__x = x
        self.__y = y

        # if color isn't specified, make a black pixel
        if color is None:
            self.__color = Color(0, 0, 0)
        else:
            self.set_color(color)

    def copy(self):
        """Returns a copy of this Pixel object."""
        return Pixel(self.__color, self.__x, self.__y)

    def get_rgb(self):
        """Returns color of pixel as an (r, g, b) tuple."""
        return self.__color.get_rgb()

    def get_color(self):
        """Returns color of pixel."""
        return self.__color

    def get_red(self):
        """Returns red component of pixel."""
        return self.__color.get_red()

    def get_green(self):
        """Returns green component of pixel."""
        return self.__color.get_green()

    def get_blue(self):
        """Returns blue component of pixel."""
        return self.__color.get_blue()

    def get_x(self):
        """Returns x value of Pixel's location."""
        return self.__x

    def get_y(self):
        """Returns y value of Pixel's location."""
        return self.__y

    def set_red(self, new_red):
        """Changes value of red component."""
        self.__color.set_red(new_red)

    def set_green(self, new_green):
        """Changes value of green component."""
        self.__color.set_green(new_green)

    def set_blue(self, new_blue):
        """Changes value of blue component."""
        self.__color.set_blue(new_blue)

    def set_color(self, new_color):
        """
        Changes color of this Pixel.

        The new color may be either a Color object, a Pixel object, or a tuple
        with (r, g, b) values.
        """
        if isinstance(new_color, Color):
            # If this is a Color object, set our color variable to a copy of it
            self.__color = new_color.copy()
        elif isinstance(new_color, tuple):
            # if its a tuple, make a Color object first
            if len(new_color) != 3:
                raise ValueError("color tuple must be in format (r, g, b)")
            self.__color = Color(new_color[0], new_color[1], new_color[2])
        elif isinstance(new_color, Pixel):
            # if its a Pixel, create new Color object from its RGB
            self.__color = Color(new_color.get_red(), new_color.get_green(), new_color.get_blue())
        else:
            raise TypeError("color must be given as a Color, Pixel, or RGB tuple.")

    def __str__(self):
        rgb = self.__color.get_rgb()
        return "Pixel at (%d, %d) with red=%d, green=%d, blue=%d" % (self.__x,
                self.__y, rgb[0], rgb[1], rgb[2])

    def __eq__(self, other):
        """
        Checks for equality of this pixel and another one.

        Two pixels are considered equal if both their location and their colors
        are the same.
        """
        return self.__x == other.get_x() \
                and self.__y == other.get_y() \
                and self.__color == other.get_color()

    def __ne__(self, other):
        return self.__x != other.get_x() \
                or self.__y != other.get_y() \
                or self.__color != other.get_color()

    # camelCase alternative naves
    getRGB = get_rgb
    getColor = get_color
    getRed = get_red
    getGreen = get_green
    getBlue = get_blue
    getX = get_x
    getY = get_y
    setRed = set_red
    setGreen = set_green
    setBlue = set_blue
    setColor = set_color


class Picture:
    """This class represents a digital picture/image."""

    def __init__(self, width=100, height=100, title=None, pic=None, filename=None):

        if pic is not None:
            # If we were given an existing pic, then create a copy of that
            self.__width = pic.get_width()
            self.__height = pic.get_height()
            self.__pixels = [[Pixel(pic.get_pixel(x, y), x, y) for x in
                range(self.__width)] for y in range(self.__height)]
            self.__title = pic.get_title()

        elif filename is not None:
            # If we are given a filename, then open that file and read in
            image = Image.open(filename)
            self.__width = image.width
            self.__height = image.height

            def get_image_pixel(img, x, y):
                """Returns Pixel with color of pixel at (x,y) in given image."""
                if img.mode == "RGB":
                    color = img.getpixel((x,y))
                elif img.mode == "L":
                    # luminence is grayscale... given as a single value
                    l = img.getpixel((x,y))
                    color = (l, l, l)
                else:
                    print(img.mode)
                    raise RuntimeError("Image in %s has unsupported mode: %s" %
                            (filename, img.mode))

                return Pixel(color, x, y)

            self.__pixels = [[get_image_pixel(image, x, y) 
                for x in range(self.__width)] for y in range(self.__height)]
            self.__title = title

        else:
            # If we weren't given an existing pic, create a new blank one of the
            # specified width and height.
            self.__width = width
            self.__height = height
            self.__pixels = [[Pixel(Black, x, y) for x in range(width)] for y in range(height)]
            self.__title = title

    def copy(self):
        """Returns a copy of this Pixel object."""
        return Picture(pic=self)

    def get_pixel(self, x, y):
        """Returns Pixel object at the specified (x,y) coordinates."""
        return self.__pixels[y][x]

    def set_color(self, x, y, color):
        """
        Changes the color of the Pixel object at the specified (x,y) coordinates.

        The color paramater may be a Pixel, a Color, or an (r, g, b) tuple.
        """
        self.__pixels[y][x].set_color(color)

    def get_title(self):
        return self.__title

    def set_title(self, new_title):
        self.__title = new_title

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def show(self):
        """Displays the picture in a new window."""
        #window = Toplevel()
        """
        window = Tk()

        if self.__title is not None:
            window.title(self.__title)

        canvas = Canvas(window, width=self.__width, height=self.__height)

        def print_pixel(event):
            print(self.get_pixel(event.x, event.y))

        canvas.bind('<Button-1>', print_pixel) # bind left-click to printing pixel info
        canvas.pack()

        img = self.__get_image(window)
        canvas.create_image((self.__width/2, self.__height/2), image=img, state="normal")

        window.mainloop()
        """

        img = []
        for y in range(self.__height):
            img.append([self.__pixels[y][x].get_rgb()
                        for x in range(self.__width)])

        ax = plt.imshow(img)
        plt.tick_params(axis='x', bottom=False, top=True, labelbottom=False,
                        labeltop=True)
        #ax.xaxis.tick_top()
        plt.show()

    def save(self, filename):
        """ Saves this picture to a file with the given file name. """
        img = Image.new('RGB', (self.__width, self.__height), 255)
        data = img.load()

        for x in range(self.__width):
            for y in range(self.__height):
                data[x,y] = self.get_pixel(x,y).get_rgb()

        img.save(filename)

    def __get_image(self, win):
        """Returns this picture as a Tkinter PhotoImage object."""
        img = PhotoImage(master=win, width=self.__width, height=self.__height)
        for x in range(self.__width):
            for y in range(self.__height):
                curr_pixel = self.__pixels[y][x]
                img.put("#%02x%02x%02x" % curr_pixel.get_rgb(), (x, y))

        return img

    def __str__(self):
        return "A picture with width = %d and height = %d" % (self.__width,
                self.__height)

    def __eq__(self, other):
        """
        Checks for equality of this Picture and another one.

        Two Pictures are considered equal if the colors of all their pixels are
        the same. The title of the pictures may differ between equal Picture
        objects though.
        """
        if self.__width != other.get_width() \
                or self.__height != other.get_height():
                    return False

        # check all individual pixels for equality
        for x in range(self.__width):
            for y in range(self.__height):
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


    # camelCase alternative naves
    getPixel = get_pixel
    setColor = set_color
    getTitle = get_title
    setTitle = set_title
    getWidth = get_width
    getHeight = get_height
    setPixel = set_color


if __name__ == "__main__":
    pic = Picture(100, 150)

    # create color gradient in picture
    for x in range(pic.get_width()):
        for y in range(pic.get_height()):
            pic.set_color(x, y, (x % 256, y % 256, x+y % 256))

    pic.set_title("Color Gradient")

    pic.show()

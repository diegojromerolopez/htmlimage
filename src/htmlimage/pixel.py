# -*- coding: utf-8 -*-

class Pixel(object):
    """
    Representes each one of the pixels of the image in RGB format
    """

    @staticmethod
    def _pad_hex_value(h):
        """
        Pads a hex value prepending 0s if its value is less than 10 (in hexadecimal).
        """

        if len(h) < 2:
            return u"0{0}".format(h)
        return h


    @staticmethod
    def _dec_to_hex(color):
        """
        Converts a decimal color value (0-255) to hexadecimal.
        Note the resulting value is padded with zeros.
        """

        return Pixel._pad_hex_value(format(color, "x"))


    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


    def to_hex_string(self):
        """
        Converts a pixel to its hexadecimal representation.
        """
        hex_r = Pixel._dec_to_hex(self.r)
        hex_g = Pixel._dec_to_hex(self.g)
        hex_b = Pixel._dec_to_hex(self.b)
        return "{hex_r}{hex_g}{hex_b}".format(hex_r=hex_r, hex_b=hex_b, hex_g=hex_g)


    def __unicode__(self):
        return self.to_hex_string()


    def __str__(self):
        return self.to_hex_string()

    @staticmethod
    def avg_pixels(pixels):
        """
        Computes de average pixel from a list of pixels.
        """
        sum_r = 0
        sum_g = 0
        sum_b = 0
        for pixel in pixels:
            sum_r += pixel.r
            sum_g += pixel.g
            sum_b += pixel.b
        num_pixels = len(pixels)
        return Pixel(r=sum_r/num_pixels, g=sum_g/num_pixels, b=sum_b/num_pixels)


    def avg(self, pixels):
        """
        Computes de average pixel between the current pixel and the parameters.
        """
        return Pixel.avg_pixels([self] + pixels)


    def abs_diff(self, pixel):
        """
        Computes the absolute difference between the colors of two pixels.
        Returns a tuple of three componentes containing the absolute difference
        for each color (red, green and blue).
        """
        diff_r = abs(self.r - pixel.r)
        diff_g = abs(self.g - pixel.g)
        diff_b = abs(self.b - pixel.b)
        return (diff_r, diff_g, diff_b)

# -*- coding: utf-8 -*-

from PIL import Image
import numpy
from pixel import Pixel


class HtmlImageEmbedder(object):
    """
    Converts a image in a series of HTML code that looks like an image
    but it's not.

    This is only a pastime and has no further utility other than understanding
    that this method renders an image that weights 1000 times more than the
    original image.

    Why did I do this?

    To test if gzip compression of this kind of "image" could come close to
    a JPG image (note: it doesn't). It also tests if could be an interesting way
    of showing embeded images in email clients like GMail that doesn't support
    data URIs (note: it isn't).

    See https://www.campaignmonitor.com/blog/email-marketing/2013/02/embedded-images-in-html-email/
    for more information about image embedding in HTML emails with data URIs.
    """

    ## HTML template for each pixel
    PIXEL_HTML_TEMPLATE = "<span style='display:inline-block;width:{w}px;height:{h}px;background-color:#{hex_pixel};'></span>"


    def __init__(self, name, image_path):
        self.name = name
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.rgb_image = self.image.convert('RGB')
        self.width = self.image.width
        self.height = self.image.height


    def _get_pixel(self, i, j):
        """
        Gets image pixel in position (i, j) as a tuple of RGB
        """
        r, g, b = self.rgb_image.getpixel((i, j))
        return Pixel(r, g, b)


    @staticmethod
    def _convert_pixel_to_html(pixel, w_size=1, h_size=1):
        """
        Converts an RGB value with a given width and height to its HTML
        representation.
        """

        hex_pixel = pixel.to_hex_string()
        pixel_html = HtmlImageEmbedder.PIXEL_HTML_TEMPLATE.format(w=w_size,h=h_size,hex_pixel=hex_pixel)
        return pixel_html


    def _get_pixel_in_html(self, i, j):
        """
        Gets the representation of pixel i, j in HTML.
        """

        pixel = self._get_pixel(i, j)
        pixel_html = HtmlImageEmbedder._convert_pixel_to_html(pixel)
        return pixel_html


    def convert_to_html(self):
        """
        Creates a new HTML image that is a clone pixel by pixel
        of the original image.
        """

        html = "<div>\n"
        for j in xrange(0, self.height):
            html += "<div>"
            for i in xrange(0, self.width):
                pixel_html = self._get_pixel_in_html(i, j)
                html += pixel_html
            html += "</div>\n"
        html += "</div>\n"
        return html


    def save_to_html(self, output_path, compression=None):
        """
        Saves the image in HTML in the chosen output path.
        """
        html_image = self.convert_to_html()

        with open(output_path, 'w') as output_file:
            output_file.write(html_image)

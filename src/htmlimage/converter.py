# -*- coding: utf-8 -*-

from PIL import Image


class HtmlImageConverter:
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
    PIXEL_HTML_TEMPLATE = "<span style='display:inline-block;width:{w}px;height:{h}px;background-color:#{r}{g}{b};'></span>"


    def __init__(self, name, image_path):
        self.name = name
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.rgb_image = self.image.convert('RGB')
        self.width = self.image.width
        self.height = self.image.height


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
        Converts a decimal value to hexadecimal.
        Note the resulting value is padded with zeros.
        """

        return HtmlImageConverter._pad_hex_value(format(color, "x"))


    def _get_rgb_pixel(self, i, j):
        r, g, b = self.rgb_image.getpixel((i, j))
        return (r, g, b)


    @staticmethod
    def _convert_rgb_pixel_to_html(r, g, b, w_size=1, h_size=1):
        """
        Converts an RGB value with a given width and height to its HTML
        representation.
        """

        hex_r = HtmlImageConverter._dec_to_hex(r)
        hex_g = HtmlImageConverter._dec_to_hex(g)
        hex_b = HtmlImageConverter._dec_to_hex(b)
        pixel_html = HtmlImageConverter.PIXEL_HTML_TEMPLATE.format(w=w_size,h=h_size,r=hex_r,g=hex_g,b=hex_b)
        return pixel_html


    def _get_pixel_in_html(self, i, j):
        """
        Gets the representation of pixel i, j in HTML.
        """

        r, g, b = self._get_rgb_pixel(i, j)
        pixel_html = HtmlImageConverter._convert_rgb_pixel_to_html(r, g, b)
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


    def convert_to_avg_html(self, r_threshold=75, b_threshold=55, g_threshold=50):
        """
        Creates a new HTML image that is built by averaging pixels horizontally
        that don't pass the threshold for each color independently
        """

        html = "<div>\n"
        for j in xrange(0, self.height):
            html += "<div>"
            i = 0
            while i < self.width:
                r, g, b = self._get_rgb_pixel(i, j)

                total_r = 0
                total_g = 0
                total_b = 0

                num_steps_taken = 0
                s = 0
                threshold_passed = False
                while i + s < self.width and not threshold_passed:
                    i_s = i + s
                    r_s, g_s, b_s = self._get_rgb_pixel(i_s, j)
                    if abs(r-r_s) < r_threshold and abs(g-g_s) < g_threshold and abs(b-b_s) < b_threshold:
                        total_r += r_s
                        total_g += g_s
                        total_b += b_s
                        num_steps_taken += 1
                    else:
                        threshold_passed = True
                    s += 1

                avg_r = total_r / num_steps_taken
                avg_g = total_g / num_steps_taken
                avg_b = total_b / num_steps_taken
                pixel_html = HtmlImageConverter._convert_rgb_pixel_to_html(avg_r, avg_g, avg_b, w_size=num_steps_taken)
                html += pixel_html
                i += num_steps_taken

            html += "</div>\n"
        html += "</div>\n"
        return html


    def save_to_html(self, output_path, compression=None):
        """"
        Saves the image in HTML in the chosen output path.
        """"
        if compression:
            if compression == "avg":
                html_image = self.convert_to_avg_html()
            else:
                raise Exception(u"'{0}' method does not exist".format(compression))
        else:
            html_image = self.convert_to_html()

        with open(output_path, 'w') as output_file:
            output_file.write(html_image)

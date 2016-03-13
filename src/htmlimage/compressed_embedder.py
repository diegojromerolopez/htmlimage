# -*- coding: utf-8 -*-

from PIL import Image
from embedder import HtmlImageEmbedder
from pixel import Pixel


class HtmlCompressedEmbedder(HtmlImageEmbedder):

    def __init__(self, name, image_path, r_threshold=50, g_threshold=50, b_threshold=50):
        super(HtmlCompressedEmbedder, self).__init__(name, image_path)
        self.r_threshold = r_threshold
        self.g_threshold = g_threshold
        self.b_threshold = b_threshold


    def convert_to_html(self):
        """
        Creates a new HTML image that is built by averaging pixels horizontally
        that don't pass the threshold for each color independently
        """

        html = "<div>\n"
        for j in xrange(0, self.height):
            html += "<div>"
            i = 0
            while i < self.width:
                pixel_ij = self._get_pixel(i, j)

                sum_r = pixel_ij.r
                sum_g = pixel_ij.g
                sum_b = pixel_ij.b

                s = 1
                threshold_passed = False
                pixels_similar_to_pixel_ij = []
                while i + s < self.width and not threshold_passed:
                    i_s = i + s
                    #print "{0}: {1} of {2}".format(j, i_s, self.width)
                    pixel_isj = self._get_pixel(i_s, j)

                    diff_r, diff_b, diff_g = pixel_ij.abs_diff(pixel_isj)
                    if diff_r < self.r_threshold and diff_g < self.g_threshold and diff_b < self.b_threshold:
                        pixels_similar_to_pixel_ij.append(pixel_isj)
                        sum_r += pixel_isj.r
                        sum_g += pixel_isj.g
                        sum_b += pixel_isj.b
                    else:
                        threshold_passed = True
                    s += 1

                num_pixels = len(pixels_similar_to_pixel_ij) + 1
                #avg_pixel = pixel_ij.avg(pixels_similar_to_pixel_ij)
                avg_pixel = Pixel(sum_r/num_pixels, sum_g/num_pixels, sum_b/num_pixels)
                pixel_html = HtmlCompressedEmbedder._convert_pixel_to_html(avg_pixel)
                html += pixel_html
                i += 1

            html += "</div>\n"
        html += "</div>\n"
        return html

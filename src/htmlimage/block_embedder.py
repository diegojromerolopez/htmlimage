# -*- coding: utf-8 -*-

from PIL import Image
import numpy
from embedder import HtmlImageEmbedder
from pixel import Pixel


class HtmlBlockEmbedder(HtmlImageEmbedder):

    ## HTML template that represents a pixel
    PIXEL_HTML_TEMPLATE = "<td style='padding:0;width:{w}px;height:{h}px;background-color:#{hex_color};'></td>"


    def __init__(self, name, image_path, block_size=2):
        super(HtmlBlockEmbedder, self).__init__(name, image_path)
        self.block_size = block_size


    def convert_to_html(self):
        """
        Creates a new HTML image that is built by averaging blocks of pixels of
        a given size.
        """

        html = "<table style='table-layout:fixed; border-spacing: 0;width:{w}px; height:{h}px; border: 1px solid green;'>".format(w=self.width, h=self.height)

        j = 0
        while j < self.height:
            i = 0

            html += "<tr>"
            while i < self.width:

                block_pixels = []
                for jx in xrange(j, j+self.block_size+1):
                    for ix in xrange(i, i+self.block_size+1):
                        if ix < self.width and jx < self.height:
                            block_pixels.append(self._get_pixel(ix, jx))

                if len(block_pixels) > 0:
                    avg_pixel = Pixel.avg_pixels(block_pixels)
                    html += HtmlBlockEmbedder.PIXEL_HTML_TEMPLATE.format(w=self.block_size, h=self.block_size, hex_color=avg_pixel.to_hex_string())

                i += self.block_size

            j += self.block_size

            html += "</tr>"

        html += "</table>"
        return html

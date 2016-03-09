# -*- coding: utf-8 -*-

import os
import converter
import sys

if __name__ == "__main__":

    sample_index = 1
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        sample_index = int(sys.argv[1])
        if sample_index < 1 or sample_index > 3:
            raise Exception(u"Please, choose a sample image between 1 and 3.")

    print(u"Let's enconde sample image {0}".format(sample_index))

    compression = None
    if len(sys.argv) >= 3 and sys.argv[2] in ["avg"]:
        compression = sys.argv[2]

    # First test
    current_path = os.path.dirname(os.path.abspath(__file__))
    samples_dir_path = current_path+ "/../../samples"
    sample_name = "sample{0}.jpg".format(sample_index)
    sample_file_path = samples_dir_path + "/" + sample_name

    image = converter.HtmlImageConverter(sample_name, sample_file_path)
    output_file_path = samples_dir_path+"/sample{0}{1}.html".format(sample_index, compression if compression else "")
    image.save_to_html(output_file_path, compression=compression)

    print(u"Image encoded successfully")

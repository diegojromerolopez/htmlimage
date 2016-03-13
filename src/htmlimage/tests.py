# -*- coding: utf-8 -*-

import os
import embedder
import compressed_embedder
import block_embedder
#import dynamic_block_embedder
import sys

if __name__ == "__main__":

    sample_index = 1
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        sample_index = int(sys.argv[1])
        if sample_index < 1 or sample_index > 5:
            raise Exception(u"Please, choose a sample image between 1 and 5.")

    print(u"Let's enconde sample image {0}".format(sample_index))

    # First test
    current_path = os.path.dirname(os.path.abspath(__file__))
    samples_dir_path = current_path+ "/../../samples"
    sample_name = "sample{0}.jpg".format(sample_index)
    sample_file_path = samples_dir_path + "/" + sample_name

    # Basic embedded image
    image = embedder.HtmlImageEmbedder(sample_name, sample_file_path)
    output_file_path = samples_dir_path+"/sample{0}_base.html".format(sample_index)
    image.save_to_html(output_file_path)

    # Basic compressed image
    image = compressed_embedder.HtmlCompressedEmbedder(sample_name, sample_file_path, 50, 50, 50)
    output_file_path = samples_dir_path+"/sample{0}_avg.html".format(sample_index)
    image.save_to_html(output_file_path)

    # Block compressed image
    image = block_embedder.HtmlBlockEmbedder(sample_name, sample_file_path, block_size=2)
    output_file_path = samples_dir_path+"/sample{0}_block.html".format(sample_index)
    image.save_to_html(output_file_path)

    # Block compressed image
    #image = dynamic_block_embedder.HtmlDynamicBlockEmbedder(sample_name, sample_file_path, max_block_size=10)
    #output_file_path = samples_dir_path+"/sample{0}_dynamic_block.html".format(sample_index)
    #image.save_to_html(output_file_path)

    print(u"Image encoded successfully")

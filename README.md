# htmlimage

A Python library to convert images to HTML code.

## Requirements

Package requirements are in requirements.txt file.

## What's this?

The original purpose of this module was helping developers to embed images in HTML emails.

Given that there are some email clients (GMail among them) that don't show data URIs embedded images, my main aim was designing a HTML representation of images that every browser could view.

This HTML images are constructed using inline CSS styles and the <div> and <span> tags. This way each email cliente will be able to show them without any problem.

Of course this is only a pastime and the resultant images are **too big to be included in an HTML email**. It is remarkable that, for some thresholds, the horizontal-averaged image has smaller size. And that if this image is compressed, its size is similar to the one of the original JPG image.


## Notes
- Sample images are Public Domain (I'm not the author).
- This project has MIT License.
- Do not use this code in production, it is only a toy.

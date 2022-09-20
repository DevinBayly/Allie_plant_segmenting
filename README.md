# Allie_plant_segmenting

## Refresher on how the code works
The following explains a bit about how the code written for pine tree segmentation works. 


### Foregrounder.py

This program converts an image from rgb to lab color space where the separate color channels represent luminosity, yellow vs blue, and red vs green. The red vs green channel shows a decent amount of contrast for the gray background images. 

### paralleler.py

This script will invoke the foregrounder on all the png images that haven't been processed already. It accepts several arguments 

* minv
    * this is the minimum value that we will use, so values that are below this become black pixels
* maxv 
    * this is the maximum value, so values above this will become black also
* nproc
    * this is the number of simultaneous images that we can process. Note that as this value goes up we end up using more system memory and this can sometimes be too much and the processing winds up killed.


It will also print out a message that estimates the number of images yet to process. 

### zipper.py

This script just adds all the images that have the `_segmented` suffix to a zip file in the folder where the script is run. The resulting file is called seg_pass.zip


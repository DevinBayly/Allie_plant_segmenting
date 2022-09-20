
import os
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
from PIL import Image
from pathlib import Path
import argparse
import os
from skimage import io,color

parser = argparse.ArgumentParser("perform image segmentation with python")
parser.add_argument("fname")
parser.add_argument("min")
parser.add_argument("max")



args = parser.parse_args()
pth = Path(args.fname)


def procPlant(im):
  hsl = color.rgb2hsv(im)
  # use a histogram and the derivative of the values to figure out the min and the max 
  hist,edges = np.histogram(im[:,:,0],bins = 256, range = (0,256))
  d = np.diff(hist)
  minval = np.where(d == np.max(d[100:150]))[0][0]
  maxval = np.where(d ==np.min(d[100:250]))[0][0] + 10 # the +10 is to increase our margin of error for the upper limit of the red channel
    #these min max are taken from image editor when a reasonable neighborhood is found
  min_thresh = minval/255
  max_thresh = maxval/255
  inverted_hsl = 1-hsl
    # we create a mask where for each pixel we say true or false if it is less than the min thresh or above the max
    # got this part wrong the first time I typed this out.. 
  mask = (inverted_hsl[:,:,0]>max_thresh)+(inverted_hsl[:,:,0]<min_thresh)
  masked = im.copy()
  masked[mask] =0
  # this part has to do with auto cropping
  rmask=im[:,:,0] < 255 *(im[:,:,0]>200)
  gmask=im[:,:,1] < 146 *(im[:,:,1]> 45)
  bmask=im[:,:,2] < 22
  coords =np.where(rmask*gmask*bmask)
  croppoint = np.min(coords[0])- 40 # magic number, watch out!

  cropped = masked[:croppoint,:,:]

  return Image.fromarray(cropped)



date = Path(f"{pth.parents[1]}/Segmented")
date.mkdir(exist_ok=True,parents=True)
img = io.imread(pth)
output = procPlant(img)
output.save(f"{date.absolute()}/{pth.stem}_segmented.jpg")


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
    #these min max are taken from image editor when a reasonable neighborhood is found
  min_thresh = int(args.min)/255
  max_thresh = int(args.max)/255
  inverted_hsl = 1-hsl
    # we create a mask where for each pixel we say true or false if it is less than the min thresh or above the max
    # got this part wrong the first time I typed this out.. 
  mask = (inverted_hsl[:,:,0]>max_thresh)+(inverted_hsl[:,:,0]<min_thresh)
  masked = im.copy()
  masked[mask] =0
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

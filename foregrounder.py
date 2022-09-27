
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
  # use a histogram and the derivative of the values to figure out the min and the max 
  f32im= im.astype("float32")
  diff_im = (f32im[:,:,2] + f32im[:,:,1])/2 - f32im[:,:,0]
  mask = diff_im <-80
  masked = im.copy()
  masked[mask] =0
  ## makes sense to only check the lower 1/4, this will remove overzelous cropping
  quarter = 3*im.shape[0]/4
  rmask=im[:,:,0] < 255 *(im[:,:,0]>200)
  gmask=im[:,:,1] < 146 *(im[:,:,1]> 45)
  bmask=im[:,:,2] < 22
  coords =np.where(rmask*gmask*bmask)
  croppoint = np.min(coords[0][coords[0] > quarter])- 40 # magic number, watch out!

  cropped = masked[:croppoint,:,:]

  return Image.fromarray(cropped)



date = Path(f"{pth.parents[1]}/Segmented")
date.mkdir(exist_ok=True,parents=True)
img = io.imread(pth)
output = procPlant(img)
output.save(f"{date.absolute()}/{pth.stem}_segmented.jpg")

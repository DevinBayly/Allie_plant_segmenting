
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
  lab = color.rgb2lab(im)
  lab_scaled = (lab + [0, 128, 128]) / [100, 255, 255]
  values = lab_scaled[:,:,2].flatten()
  topBackground = np.max(lab_scaled[:500,:500,2])
  mask = (lab_scaled[:,:,2]<args.max)
  masked = im.copy()
  masked[mask] =0


  rmask=masked[:,:,0] < 255 *(masked[:,:,0]>200)
  gmask=masked[:,:,1] < 146 *(masked[:,:,1]> 45)
  bmask=masked[:,:,2] < 22
  coords =np.where(rmask*gmask*bmask)
  croppoint = np.min(coords[0])- 40 # magic number, watch out!

  cropped = masked[:croppoint,:,:]

  return Image.fromarray(cropped)





date = Path(f"{pth.parents[1]}/Segmented")
date.mkdir(exist_ok=True,parents=True)
print(f"{pth}")
img = io.imread(pth)
output = procPlant(img)
output.save(f"{date.absolute()}/{pth.stem}_segmented.jpg")


import multiprocessing as mp
import argparse
from pathlib import Path
import os
import subprocess as sp

def run_foregrounder(img_name,minv,maxv):
  sp.run(f"python3 foregrounder.py '{img_name}' {minv} {maxv}",shell=True)

images = []

parser = argparse.ArgumentParser()
parser.add_argument("folder",default="./")
parser.add_argument("minv",default="159")
parser.add_argument("maxv",default="236")
parser.add_argument("num_proc",default="4")

args = parser.parse_args()

segs =[]
print(os.getcwd())
for pth,sub,fls in os.walk(args.folder):
  for fl in fls:
    if "_segmented" in fl:
      segs.append(fl.replace("_segmented","").lower())
total = []
processed  = []
for pth,sub,fls in os.walk(args.folder):
  for fl in fls:
    fl_lower = fl.lower()
    if "jpg" in fl_lower and not "_segmented" in fl_lower:
      total.append(fl_lower)
      if fl_lower not in segs:
        images.append(pth+"/"+fl)
      else:
        processed.append(fl_lower)

print("total ", len(total), "processed ",len(processed), len(images),"still to process")
with mp.Pool(int(args.nproc)) as p:
  p.map(run_foregrounder,images)

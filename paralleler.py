
import multiprocessing as mp
import argparse
from pathlib import Path
import os
import subprocess as sp

def run_foregrounder(vals):
  img_name = vals[0]
  minv = vals[1]
  maxv = vals[2]
  sp.run(f"python3 foregrounder.py '{img_name}' {minv} {maxv}",shell=True)

images = []

parser = argparse.ArgumentParser()
parser.add_argument("folder",default="./")
parser.add_argument("--minv",default="159",required=False)
parser.add_argument("--maxv",default="255",required=False)
parser.add_argument("--nproc",default="4",required=False)

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
  p.map(run_foregrounder,[(i,args.minv,args.maxv) for i in images])

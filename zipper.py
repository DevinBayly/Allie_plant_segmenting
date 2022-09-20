import os
import zipfile as zf

with zf.ZipFile("seg_pass.zip","w") as phile:
  for pth,sub,fls in os.walk("./"):
    for fl in fls:
      if "_segmented" in fl.lower():
        phile.write(pth+"/"+ fl)


  

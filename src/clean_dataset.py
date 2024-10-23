import numpy as np
import os

path = "images/IBUG_image_"

for i in range(31, 120):
  n_image = str(i)
  if i < 10:
    n_image = "00" + n_image
  elif i < 100:
    n_image = "0" + n_image

  for j in range(0, 6):
    file_path = f"{path}{n_image}_{j}.jpg"
    file_path2 = f"{path}{n_image}_1_{j}.jpg"
    if os.path.exists(file_path):
      os.remove(file_path)
    if os.path.exists(file_path2):
      os.remove(file_path2)
    
  

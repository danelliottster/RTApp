import sys
sys.path += ["c:/Users/segana/source/repos/"]
import RTApp_tools
from RTApp_tools import Mask , CTdata
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

DV = CTdata();

data_path = "e:/SegAnaData/data/2.16.840.1.114362.1.11785856.22499700301.500187548.274.9110/output/iso_image_0_aligned"

DV.load_from_Segana(data_path+".params" , data_path+".raw.gz")

fig,slider = RTApp_tools.visualize.view_volume(DV,vmin=np.min(DV.data),vmax=np.max(DV.data))

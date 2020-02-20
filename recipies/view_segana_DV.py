import sys
sys.path += ["c:/Users/segana/source/repos/"]
import RTApp_tools
from RTApp_tools import Mask , CTdata
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

DV = CTdata();
# DV.load_from_Segana("e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/iso_image_0_dose.params" , "e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/iso_image_0_dose.raw.gz")
DV.load_from_Segana("e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/rtdose.params" , "e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/rtdose.raw.gz")

fig,slider = RTApp_tools.visualize.view_volume(DV,vmin=np.min(DV.data),vmax=np.max(DV.data))

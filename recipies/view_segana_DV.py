import sys
sys.path += ["c:/Users/segana/source/repos/"]
import RTApp_tools
from RTApp_tools import Mask , CTdata
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

DV = CTdata();

DV.load_from_Segana("e:/SegAnaData/data/1.2.246.352.221.477049225889020498914422815209278789030/output/TRACE_pre_isotropic_post_maskiso_sim.params" , "e:/SegAnaData/data/1.2.246.352.221.477049225889020498914422815209278789030/output/TRACE_pre_isotropic_post_maskiso_sim.raw.gz")

fig,slider = RTApp_tools.visualize.view_volume(DV,vmin=np.min(DV.data),vmax=np.max(DV.data))

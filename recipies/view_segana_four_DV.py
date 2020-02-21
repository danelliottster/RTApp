import sys
sys.path += ["c:/Users/segana/source/repos/"]
import RTApp_tools
from RTApp_tools import Mask , CTdata
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

DV1 = CTdata(); DV2 = CTdata(); DV3 = CTdata(); DV4 = CTdata();
DV1.load_from_Segana("e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/debug_register_target_after_read.params" , "e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/debug_register_target_after_read.raw.gz")
DV2.load_from_Segana("e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/debug_register_target_subvolume.params" , "e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/debug_register_target_subvolume.raw.gz")
DV3.load_from_Segana("e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/debug_register_target_after_normalization.params" , "e:/SegAnaData/data/1.2.840.113704.1.111.5268.1496951889.14/output/debug_register_target_after_normalization.raw.gz")

fig,slider = RTApp_tools.visualize.compare_four_volumes_dynamic(DV1, DV1 , DV2, DV3)

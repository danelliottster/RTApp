import sys
sys.path += ["c:/Users/segana/source/repos/"]
import RTApp_tools
from RTApp_tools import Mask , CTdata , RTVolume
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

do_overlay = True
W_max = 5.0
arrow_spacing = 4
frac_num = 0
output_path = "e:/SegAnaData/data/2.16.840.1.114362.1.6.6.5.16628.12077178638.497684152.567.1/output"
U_path = output_path + "/iso_image_"+str(frac_num)+"_u_dvf"
V_path = output_path + "/iso_image_"+str(frac_num)+"_v_dvf"
W_path = output_path + "/iso_image_"+str(frac_num)+"_w_dvf"
# U_path = output_path + "/iso_image_"+str(frac_num)+"_cb2kv_u_dvf"
# V_path = output_path + "/iso_image_"+str(frac_num)+"_cb2kv_v_dvf"
# W_path = output_path + "/iso_image_"+str(frac_num)+"_cb2kv_w_dvf"
source_path = output_path+"/iso_sim"
target_path = output_path+"/iso_image_"+str(frac_num)+"_aligned"

DVF_U = RTVolume(); DVF_V = RTVolume(); DVF_W = RTVolume();
DVF_U.load_from_Segana( U_path+".params" , U_path+".raw.gz")
DVF_V.load_from_Segana( V_path+".params" , V_path+".raw.gz")
DVF_W.load_from_Segana( W_path+".params" , W_path+".raw.gz")

CT_source = CTdata(); CT_target =  None
CT_source.load_from_Segana( source_path+".params" , source_path+".raw.gz" )
if do_overlay:
    CT_target = CTdata();
    CT_target.load_from_Segana( target_path+".params" , target_path+".raw.gz" )

fig,slider = RTApp_tools.visualize.DVF.all_views_dynamic( DVF_U , DVF_V , DVF_W ,
                                                          CT_source , CT_target ,
                                                          arrow_spacing = arrow_spacing)

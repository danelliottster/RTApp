import sys
sys.path += ["c:/Users/segana/source/repos/"]
import RTApp_tools as rtt
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np

data_dir = "e:/SegAnaData/data/1.2.246.352.221.542146033641418762011679416712589851569/output/"
frac_num = 0
ROI_name = "Cochlea_L"
max_dose_gy = 70.0

deformed_mask = rtt.Mask(); plan_mask = rtt.Mask();
deformed_dose = rtt.RTVolume(); plan_dose = rtt.RTVolume(); sum_dose = rtt.RTVolume();

deformed_mask_path = data_dir + "deformed_structure_voxel_mask_iso_image_"+str(frac_num)+"_"+ROI_name
plan_mask_file = data_dir + "structure_voxel_mask_"+ROI_name
deformed_mask.load_from_Segana( deformed_mask_path+".params" , deformed_mask_path+".raw.gz" )
plan_mask.load_from_Segana( plan_mask_file+".params" , plan_mask_file+".raw.gz" )

deformed_dose_path = data_dir+"iso_image_"+str(frac_num)+"_dose"
sum_dose_path = data_dir+"sum_dose_"+str(frac_num)
plan_dose_path = data_dir+"rtdose"
deformed_dose.load_from_Segana( deformed_dose_path+".params" , deformed_dose_path+".raw.gz" )
sum_dose.load_from_Segana( sum_dose_path+".params" , sum_dose_path+".raw.gz" )
plan_dose.load_from_Segana( plan_dose_path+".params" , plan_dose_path+".raw.gz" )

mask_dose_plan_plan , dose_vals_plan_plan = rtt.dvh.compute_mask_dose( plan_mask , plan_dose )
mask_dose_def_plan , dose_vals_def_plan = rtt.dvh.compute_mask_dose( deformed_mask , plan_dose )
mask_dose_plan_def , dose_vals_plan_def = rtt.dvh.compute_mask_dose( plan_mask , deformed_dose )
mask_dose_plan_sum , dose_vals_plan_sum = rtt.dvh.compute_mask_dose( plan_mask , sum_dose )

#
# plot the four differential histograms in one figure
plan_mask_num_vox = np.sum(plan_mask.data)
def_mask_num_vox = np.sum(deformed_mask.data)
fig,ax = plt.subplots(nrows=2,ncols=2)
plan_plan_dvh = ax[0][0].hist( dose_vals_plan_plan , bins=100 )
def_plan_dvh = ax[0][1].hist( dose_vals_def_plan , bins=100 )
plan_def_dvh = ax[1][0].hist( dose_vals_plan_def , bins=100 )
plan_sum_dvh = ax[1][1].hist( dose_vals_plan_sum , bins=100 )
ax[0][0].set_title("plan struct/plan dose");
ax[0][1].set_title("def struct/plan dose");
ax[1][0].set_title("plan struct/def dose");
ax[1][1].set_title("plan struct/sum dose");
yticks = ax[0][0].get_yticks();
yticks /= float(dose_vals_plan_plan.shape[0]);
ax[0][0].set_yticklabels([str(i) for i in yticks],minor=False)
# num_vox_plan_ticks = np.arange(0,plan_mask_num_vox+1,step=plan_mask_num_vox*0.2)
# num_vox_def_ticks = np.arange(0,def_mask_num_vox+1,step=def_mask_num_vox*0.2)
# ax[0][0].set_yticks( num_vox_plan_ticks ); ax[0][0].set_yticklabels([str(num_vox/plan_mask_num_vox) for num_vox in num_vox_plan_ticks] )
# ax[1][0].set_yticks( num_vox_def_ticks ); ax[1][0].set_yticklabels([str(num_vox/plan_mask_num_vox) for num_vox in num_vox_def_ticks] )
# ax[0][1].set_yticks( num_vox_plan_ticks ); ax[0][1].set_yticklabels([str(num_vox/def_mask_num_vox) for num_vox in num_vox_plan_ticks] )
# ax[1][1].set_yticks( num_vox_plan_ticks ); ax[1][1].set_yticklabels([str(num_vox/plan_mask_num_vox) for num_vox in num_vox_plan_ticks] )
fig.show()
# done
#

#
# plot the four cumulative histograms in one figure

# # convert to percentages
# cum_dose_vals_plan_plan = dose_vals_plan_plan / float(len(dose_vals_plan_plan))
# # convert to cumulative
# cum_dose_vals_plan_plan = np.cumsum(cum_dose_vals_plan_plan)
# # convert to cumulative running the opposite direction
# cum_dose_vals_plan_plan = 100. - cum_dose_vals_plan_plan
# # do the plotting stuff

plan_mask_num_vox = np.sum(plan_mask.data)
def_mask_num_vox = np.sum(deformed_mask.data)
fig,ax = plt.subplots(nrows=2,ncols=2)
plan_plan_dvh = ax[0][0].hist( dose_vals_plan_plan , bins=100 , cumulative=-1 , range=(0,max_dose_gy))
def_plan_dvh = ax[0][1].hist( dose_vals_def_plan , bins=100  , cumulative=-1 , range=(0,max_dose_gy))
plan_def_dvh = ax[1][0].hist( dose_vals_plan_def , bins=100  , cumulative=-1 , range=(0,max_dose_gy))
plan_sum_dvh = ax[1][1].hist( dose_vals_plan_sum , bins=100  , cumulative=-1 , range=(0,max_dose_gy))
ax[0][0].set_title("plan/plan"); ax[0][1].set_title("def/plan");
ax[1][0].set_title("plan/def"); ax[1][1].set_title("plan/sum");
# num_vox_plan_ticks = np.arange(0,plan_mask_num_vox+1,step=plan_mask_num_vox*0.2)
# num_vox_def_ticks = np.arange(0,def_mask_num_vox+1,step=def_mask_num_vox*0.2)
# ax[0][0].set_yticks( num_vox_plan_ticks ); ax[0][0].set_yticklabels([str(num_vox/plan_mask_num_vox) for num_vox in num_vox_plan_ticks] )
# ax[1][0].set_yticks( num_vox_def_ticks ); ax[1][0].set_yticklabels([str(num_vox/plan_mask_num_vox) for num_vox in num_vox_def_ticks] )
# ax[0][1].set_yticks( num_vox_plan_ticks ); ax[0][1].set_yticklabels([str(num_vox/def_mask_num_vox) for num_vox in num_vox_plan_ticks] )
# ax[1][1].set_yticks( num_vox_plan_ticks ); ax[1][1].set_yticklabels([str(num_vox/plan_mask_num_vox) for num_vox in num_vox_plan_ticks] )
fig.show()


# done
# 

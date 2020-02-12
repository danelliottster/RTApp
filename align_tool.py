import time
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt

def run_align_tool( volone , voltwo):

    axial_data_1 = volone.data; axial_data_2 = voltwo.data;
    sagittal_data_1 = np.swapaxes(volone.data,0,2); sagittal_data_2 = np.swapaxes(voltwo.data,0,2);
    coronal_data_1 = np.swapaxes(volone.data,0,1); coronal_data_2 = np.swapaxes(voltwo.data,0,1);

    middle_slice = int(volone.array_sz[0] / 2.)

    fig, ax = plt.subplots(nrows=1,ncols=3)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    fig.suptitle("Compare two volumes")

    axial_img = ax[0].imshow( volone.data[middle_slice,:,:] , cmap=plt.cm.gray )
    axial_img_overlay = ax[0].imshow( voltwo.data[middle_slice,:,:] , cmap=plt.cm.gray )
    sagittal_img = ax[1].imshow( np.swapaxes(volone.data,0,2)[middle_slice,:,:] , cmap=plt.cm.gray )
    sagittal_img_overlay = ax[1].imshow( np.swapaxes(voltwo.data,0,2)[middle_slice,:,:] , cmap=plt.cm.gray )
    coronal_img = ax[1].imshow( np.swapaxes(volone.data,0,1)[middle_slice,:,:] , cmap=plt.cm.gray )
    coronal_img_overlay = ax[1].imshow( np.swapaxes(voltwo.data,0,1)[middle_slice,:,:] , cmap=plt.cm.gray )

    axcolor = 'lightgoldenrodyellow'
    axslider_x = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    axslider_y = plt.axes([0.25, 0.06, 0.65, 0.03] , facecolor=axcolor)
    axslider_z = plt.axes([0.25, 0.02, 0.65, 0.03] , facecolor=axcolor)
    shift_slider_x = Slider(axslider_x , 'Slice' ,
                            -int(volone.array_sz[2]/2.) , int(volone.array_sz[2]/2.) , valinit=0)
    shift_slider_y = Slider(axslider_y , 'Slice' ,
                            -int(volone.array_sz[1]/2.) , int(volone.array_sz[1]/2.) , valinit=0)
    shift_slider_z = Slider(axslider_z , 'Slice' ,
                            -int(volone.array_sz[0]/2.) , int(volone.array_sz[0]/2.) , valinit=0)

    def update(val):
        shift_x = int(slice_slider_x.val)
        shift_y = int(slice_slider_y.val)
        shift_z = int(slice_slider_z.val)

        axial_voltwo_tmp = np.roll(voltwo.data , shift_x , axis=2)
        axial_voltwo_tmp = np.roll(axial_voltwo_tmp , shift_y , axis=1)
        axial_volone_tmp = np.roll(volone.data , shift_z , axis=0)
        axial_img.set_data(axial_volone_tmp[middle_slice,:,:])
        axial_img_overlay.set_data(axial_voltwo_tmp[middle_slice,:,:])

        sagittal_voltwo_tmp = np.roll(voltwo.data , shift_y , axis=1)
        sagittal_voltwo_tmp = np.roll(sagittal_voltwo_tmp , shift_z , axis=0)
        sagittal_volone_tmp = np.roll(voltwo.data , shift_x , axis=2)
        sagittal_img.set_data(sagittal_volone_tmp[middle_slice,:,:])
        sagittal_img_overlay.set_data(sagittal_voltwo_tmp[middle_slice,:,:])

        coronal_voltwo_tmp = np.roll(voltwo.data , shift_x , axis=1)
        coronal_voltwo_tmp = np.roll(coronal_voltwo_tmp , shift_z , axis=0)
        coronal_volone_tmp = np.roll(voltwo.data , shift_y , axis=1)
        coronal_img.set_data(coronal_volone_tmp[middle_slice,:,:])
        coronal_img_overlay.set_data(coronal_voltwo_tmp[middle_slice,:,:])

        print slice_x , slice_y , slice_z
        fig.canvas.draw_idle()

    slice_slider_x.on_changed(update)
    slice_slider_y.on_changed(update)
    slice_slider_z.on_changed(update)

    plt.show()
    plt.pause(1.)

    return fig, slice_slider_x , slice_slider_y , slice_slider_z

import time
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt

"""
assumes two volumes have same number of slices/slice positions
"""
def view_volume(vol,vmin=-1000,vmax=1024):
    middle_slice = int(vol.array_sz[0] / 2.)
    fig, ax = plt.subplots(nrows=1,ncols=1)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    img = ax.imshow( vol.data[middle_slice,:,:] , cmap=plt.cm.gray , vmin=vmin , vmax=vmax)
    fig.suptitle("Compare two volumes")
    axcolor = 'lightgoldenrodyellow'
    axslider = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    slice_slider = Slider(axslider , 'Slice' , 0.1 , vol.array_sz[0]-1 , valinit=middle_slice)

    def update(val):
        slice_i = int(slice_slider.val)
        img.set_data(vol.data[slice_i,:,:])
        fig.canvas.draw_idle()

    slice_slider.on_changed(update)

    plt.show()
    # raw_input("blocking...")
    # time.sleep(4)
    plt.pause(1.)

    return fig, slice_slider

def compare_two_volumes_dynamic( volone , voltwo):
    middle_slice = int(volone.array_sz[0] / 2.)
    fig, ax = plt.subplots(nrows=1,ncols=2)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    volone_img = ax[0].imshow( volone.data[middle_slice,:,:] , cmap=plt.cm.gray )
    voltwo_img = ax[1].imshow( voltwo.data[middle_slice,:,:] , cmap=plt.cm.gray )
    fig.suptitle("Compare two volumes")
    axcolor = 'lightgoldenrodyellow'
    axslider = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    slice_slider = Slider(axslider , 'Slice' , 0.1 , volone.array_sz[0]-1 , valinit=middle_slice)

    def update(val):
        slice_i = int(slice_slider.val)
        volone_img.set_data(volone.data[slice_i,:,:])
        voltwo_img.set_data(voltwo.data[slice_i,:,:])
        fig.canvas.draw_idle()

    slice_slider.on_changed(update)

    plt.show()
    plt.pause(1.)

    return fig, slice_slider

def compare_four_volumes_dynamic( volone , voltwo , volthree , volfour , vmin=-1024 , vmax=1024):
    middle_slice = int(volone.array_sz[0] / 2.)
    fig, ax = plt.subplots(nrows=2,ncols=2)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    volone_img = ax[0][0].imshow( volone.data[middle_slice,:,:] , cmap=plt.cm.gray , vmin=vmin , vmax=vmax )
    voltwo_img = ax[0][1].imshow( voltwo.data[middle_slice,:,:] , cmap=plt.cm.gray , vmin=vmin , vmax=vmax )
    volthree_img = ax[1][0].imshow( volthree.data[middle_slice,:,:] , cmap=plt.cm.gray , vmin=vmin , vmax=vmax )
    volfour_img = ax[1][1].imshow( volfour.data[middle_slice,:,:] , cmap=plt.cm.gray , vmin=vmin , vmax=vmax )
    axcolor = 'lightgoldenrodyellow'
    axslider = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    slice_slider = Slider(axslider , 'Slice' , 0.1 , volone.array_sz[0]-1 , valinit=middle_slice)

    def update(val):
        slice_i = int(slice_slider.val)
        volone_img.set_data(volone.data[slice_i,:,:])
        voltwo_img.set_data(voltwo.data[slice_i,:,:])
        volthree_img.set_data(volthree.data[slice_i,:,:])
        volfour_img.set_data(volfour.data[slice_i,:,:])
        fig.canvas.draw_idle()

    slice_slider.on_changed(update)

    plt.show()
    plt.pause(1.)

    return fig, slice_slider

def compare_two_slices( volone , voltwo,
                        axial_slice=None , sagittal_slice=None , coronal_slice=None):
    if not axial_slice:
        axial_slice = int(volone.array_sz[0] / 2.)
    if not sagittal_slice:
        sagittal_slice = int(volone.array_sz[2] / 2.)
    if not coronal_slice:
        coronal_slice = int(volone.array_sz[1] / 2.)

    axial_data_1 = volone.data; axial_data_2 = voltwo.data;
    sagittal_data_1 = np.swapaxes(volone.data,0,2); sagittal_data_2 = np.swapaxes(voltwo.data,0,2);
    coronal_data_1 = np.swapaxes(volone.data,0,1); coronal_data_2 = np.swapaxes(voltwo.data,0,1);

    fig, ax = plt.subplots(nrows=2,ncols=3)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    volone_axial_img = ax[0][0].imshow( axial_data_1[axial_slice,:,:] , cmap=plt.cm.gray )
    voltwo_axial_img = ax[1][0].imshow( axial_data_2[axial_slice,:,:] , cmap=plt.cm.gray )
    volone_sagittal_img = ax[0][1].imshow( sagittal_data_1[sagittal_slice,:,:] , cmap=plt.cm.gray )
    voltwo_sagittal_img = ax[1][1].imshow( sagittal_data_2[sagittal_slice,:,:] , cmap=plt.cm.gray )
    volone_coronal_img = ax[0][2].imshow( coronal_data_1[coronal_slice,:,:] , cmap=plt.cm.gray )
    voltwo_coronal_img = ax[1][2].imshow( coronal_data_2[coronal_slice,:,:] , cmap=plt.cm.gray )
    fig.suptitle("Compare two volumes, all views")

    plt.show()

    return fig

def volume_with_poly_pts(volume , poly_pts):
    middle_slice = int(volume.array_sz[0] / 2.)
    fig, ax = plt.subplots(nrows=1,ncols=1)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    img = ax.imshow( volume.data[middle_slice,:,:] , cmap=plt.cm.gray )
    fig.suptitle("Volume with polynomial points")
    axcolor = 'lightgoldenrodyellow'
    axslider = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    slice_slider = Slider(axslider , 'Slice' , 0.1 , volume.array_sz[0]-1 , valinit=middle_slice)
    line, = ax.plot([pp[0] for pp in poly_pts[middle_slice]] , [pp[1] for pp in poly_pts[middle_slice]] , "xg")
    
    def update(val):
        slice_i = int(slice_slider.val)
        img.set_data(volume.data[slice_i,:,:])
        line.set_xdata([pp[0] for pp in poly_pts[slice_i]])
        line.set_ydata([pp[1] for pp in poly_pts[slice_i]])
        fig.canvas.draw_idle()

    slice_slider.on_changed(update)

    plt.show()

    # time.sleep(4)
    plt.pause(1.)

    return fig, slice_slider

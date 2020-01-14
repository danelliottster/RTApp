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
def view_volume(vol):
    middle_slice = int(vol.array_sz[0] / 2.)
    fig, ax = plt.subplots(nrows=1,ncols=1)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    img = ax.imshow( vol.get_data()[middle_slice,:,:] , cmap=plt.cm.gray )
    fig.suptitle("Compare two volumes")
    axcolor = 'lightgoldenrodyellow'
    axslider = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    slice_slider = Slider(axslider , 'Slice' , 0.1 , vol.array_sz[0]-1 , valinit=middle_slice)

    def update(val):
        slice_i = int(slice_slider.val)
        img.set_data(vol.get_data()[slice_i,:,:])
        fig.canvas.draw_idle()

    slice_slider.on_changed(update)

    plt.show()
    # raw_input("blocking...")
    # time.sleep(4)
    plt.pause(1.)

    return fig, slice_slider

def compare_two_volumes( volone , voltwo):
    middle_slice = int(volone.array_sz[0] / 2.)
    fig, ax = plt.subplots(nrows=1,ncols=2)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    volone_img = ax[0].imshow( volone.get_data()[middle_slice,:,:] , cmap=plt.cm.gray )
    voltwo_img = ax[1].imshow( voltwo.get_data()[middle_slice,:,:] , cmap=plt.cm.gray )
    fig.suptitle("Compare two volumes")
    axcolor = 'lightgoldenrodyellow'
    axslider = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    slice_slider = Slider(axslider , 'Slice' , 0.1 , volone.array_sz[0]-1 , valinit=middle_slice)

    def update(val):
        slice_i = int(slice_slider.val)
        volone_img.set_data(volone.get_data()[slice_i,:,:])
        voltwo_img.set_data(voltwo.get_data()[slice_i,:,:])
        fig.canvas.draw_idle()

    slice_slider.on_changed(update)

    plt.show()
    # time.sleep(4)
    plt.pause(1.)

    return fig, slice_slider

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

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys
import os, itertools, copy
import numpy as np

def draw_arrows( the_axis , DVF_U , DVF_V , DVF_W , slice_num , arrow_spacing , max_mag = 5.0):
    arrow_list = []
    for pt in itertools.product(range(0,256,arrow_spacing),range(0,256,arrow_spacing)):
        if abs(DVF_U[slice_num,pt[1],pt[0]]) > 0.5 or abs(DVF_V[slice_num,pt[1],pt[0]]) > 0.5 or abs(DVF_W[slice_num,pt[1],pt[0]]) > 0.5:
            if DVF_W[slice_num,pt[1],pt[0]] < 0: # move down slices is red
                arrow_color = (min(1.0 , DVF_W[slice_num,pt[1],pt[0]]/(-max_mag)), 1, 0)
            else:               # moving up slices is blue
                arrow_color = (0 , 1 , min(1.0 , DVF_W[slice_num,pt[1],pt[0]]/max_mag))
            arrow_list += [the_axis.arrow(pt[0] , pt[1] ,
                                          DVF_U[slice_num,pt[1],pt[0]] , DVF_V[slice_num,pt[1],pt[0]] ,
                                          fc=arrow_color , ec=arrow_color , shape="full" ,
                                          head_length=0.2 , head_width=0.5 , length_includes_head=True ,
                                          alpha=0.6)]
    return arrow_list

def all_views_dynamic( U , V , W , axial_source , axial_target=None , arrow_spacing=5 , overlay_alpha=0.2 , DVF_max_range = 5.0 ):
    sagittal_target = None; coronal_target = None;

    # 
    # create sagittal and coronal views of the DVFs
    # and the source CT data
    # and, optionally, the target CT data
    # 
    sagittal_U = np.swapaxes( U.data , 0 , 2 )
    coronal_U = np.swapaxes( U.data , 0 , 1 )
    sagittal_V = np.swapaxes( V.data , 0 , 2 )
    coronal_V = np.swapaxes( V.data , 0 , 1 )
    sagittal_W = np.swapaxes( W.data , 0 , 2 )
    coronal_W = np.swapaxes( W.data , 0 , 1 )
    sagittal_source = np.swapaxes( axial_source.data , 0 , 2 )
    coronal_source = np.swapaxes( axial_source.data , 0 , 1 )
    if axial_target:
        sagittal_target = np.swapaxes(axial_target.data , 0 , 2)
        coronal_target = np.swapaxes(axial_target.data , 0 , 1)
    #
    # done
    
    #
    # create the figures and subfigures for the axial, sagittal, and coronal views
    # 
    fig, ax = plt.subplots(nrows=1,ncols=3)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    axial_img = ax[0].imshow( axial_source.data[0,:,:] , cmap=plt.cm.gray , vmin=-1000 , vmax=1000 )
    sagittal_img = ax[1].imshow( sagittal_source[0,:,:] , cmap=plt.cm.gray , vmin=-1000 , vmax=1000 )
    coronal_img = ax[2].imshow( coronal_source[0,:,:] , cmap=plt.cm.gray , vmin=-1000 , vmax=1000 )
    if axial_target:
        axial_img_target = ax[0].imshow( axial_target.data[0,:,:] , vmin=-1000 , vmax=1000 , cmap=matplotlib.cm.hot , alpha=overlay_alpha )
        sagittal_img_target = ax[1].imshow( sagittal_target[0,:,:] , vmin=-1000 , vmax=1000 , cmap=matplotlib.cm.hot , alpha=overlay_alpha )
        coronal_img_target = ax[2].imshow( coronal_target[0,:,:] , vmin=-1000 , vmax=1000 , cmap=matplotlib.cm.hot , alpha=overlay_alpha )

    axcolor = 'lightgoldenrodyellow'
    axslider = plt.axes([0.25, 0.1, 0.65, 0.03] , facecolor=axcolor)
    slice_slider = Slider( axslider , 'Slice' , 0.1 , axial_source.array_sz[2]-1 , valinit=0 )

    def update( val ):
        for arrow in update.arrows_axial:
            arrow.remove()
        for arrow in update.arrows_sagittal:
            arrow.remove()
        for arrow in update.arrows_coronal:
            arrow.remove()
        slice_i = int( slice_slider.val )
        axial_img.set_data( axial_source.data[slice_i,:,:] )
        sagittal_img.set_data( sagittal_source[slice_i,:,:] )
        coronal_img.set_data( coronal_source[slice_i,:,:] )
        if axial_target:
            axial_img_target.set_data( axial_target.data[slice_i,:,:] )
            sagittal_img_target.set_data( sagittal_target[slice_i,:,:] )
            coronal_img_target.set_data( coronal_target[slice_i,:,:] )
        update.arrows_axial=draw_arrows( ax[0],
                                         U.data ,
                                         V.data ,
                                         W.data ,
                                         slice_i ,
                                         arrow_spacing)
        update.arrows_sagittal=draw_arrows( ax[1] ,
                                            sagittal_W ,
                                            sagittal_V ,
                                            sagittal_U ,
                                            slice_i ,
                                            arrow_spacing)
        update.arrows_coronal=draw_arrows( ax[2],
                                           coronal_U ,
                                           coronal_W ,
                                           coronal_V ,
                                           slice_i ,
                                           arrow_spacing)
        fig.canvas.draw_idle()
    update.arrows_axial=[]; update.arrows_sagittal=[]; update.arrows_coronal=[]

    slice_slider.on_changed(update)

    plt.show()

    return fig , slice_slider

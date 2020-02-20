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

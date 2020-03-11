import numpy as np
import scipy.ndimage as ndimage
from . import RTVolume, Mask, utils

def compute_mask_dose( mask_in , dose_vol_in ):
    """
    Note: the Mask input, mask_in, start_pos is the distance from the starting position of the associated
    isotropically-sampled CT image
    """

    #
    # prep the output volume
    dose_mask_out = RTVolume()
    dose_mask_out.copy_metadata(mask_in)
    dose_mask_out.allocate()
    dose_mask_out.data[:] = 0   # blank it out
    # done
    # 

    #
    # get a list voxels which are in the structure (mask)
    x_idx,y_idx,z_idx = np.nonzero( mask_in.data )
    idxs = np.vstack([x_idx,y_idx,z_idx])
    idxs = idxs.astype(float)
    # done
    #

    #
    # convert the ROI voxel indices to mm positions
    # remember: the mask start position is relative to the isotropically-sampled start position
    #           will assume that the supplied dose has the same starting position
    pts_mm = mask_in.idx_to_mm(idxs)
    pts_mm += np.array([dose_vol_in.start_pos]).T
    # done
    # 

    # 
    # sample the dose at the ROI voxel positions
    pts_idx = dose_vol_in.mm_to_idx(pts_mm)
    dose_vals = dose_vol_in.sample_at_points(pts_idx)
    # done
    # 

    #
    # fill in the mask dose values
    idxs_int = idxs.astype(int)
    dose_mask_out.data[ idxs_int[0,:], idxs_int[1,:], idxs_int[2,:] ] = dose_vals
    # done
    #

    return dose_mask_out , dose_vals

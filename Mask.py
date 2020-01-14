import gzip , struct , math , copy
import numpy as np
import scipy.ndimage as ndimage
from . import utils
from . import RTVolume

# class Mask(RTVolume.RTVolume):
class Mask(RTVolume):

    # def __init__(self):
    #     RTVolume.__init__(self)

    def compute_center_of_mass_idx(self):
        # nonzeros = np.nonzero(self.data)
        # mean_row = np.mean(nonzeros[0])
        # mean_col = np.mean(nonzeros[1])
        # mean_slice = np.mean(nonzeros[2])
        # return (mean_row , mean_col , mean_slice)
        return ndimage.center_of_mass(self.data)

    def compute_center_of_mass_mm(self):
        mrow , mcol , mslice = self.compute_center_of_mass_idx()
        mm_row , mm_col , mm_slice = utils.mm_from_idx( mrow , mcol , mslice ,
                                                        self.start_pos ,
                                                        self.vox_sz )
        return ( mm_row , mm_col , mm_slice )

    def compute_volume_cc(self):
        vox_count = np.sum(self.data > 0.5)
        vol_cc = float(vox_count) * np.prod(self.vox_sz) / 1000.0
        return vol_cc
        
    def get_max_idx_each_dim(self):
        nonzeros = np.nonzero(self.data)
        max_row = np.max(nonzeros[0])
        max_col = np.max(nonzeros[1])
        max_slice = np.max(nonzeros[2])
        return ( max_row , max_col , max_slice )

    def get_min_idx_each_dim(self):
        nonzeros = np.nonzero(self.data)
        min_row = np.min(nonzeros[0])
        min_col = np.min(nonzeros[1])
        min_slice = np.min(nonzeros[2])
        return ( min_row , min_col , min_slice )

    def get_bounding_sphere(self):
        center = self.compute_center_of_mass_mm()
        max_idx = self.get_max_idx_each_dim()
        min_idx = self.get_min_idx_each_dim()
        max_mm = utils.mm_from_idx( *max_idx , start_pos = self.start_pos , vox_sz = self.vox_sz )
        min_mm = utils.mm_from_idx( *min_idx , start_pos = self.start_pos , vox_sz = self.vox_sz )
        max_dist_from_center = np.linalg.norm( np.array(max_mm) - np.array(center) )
        min_dist_from_center = np.linalg.norm( np.array(min_mm) - np.array(center) )
        radius = np.max( [abs(max_dist_from_center) , abs(min_dist_from_center)] )
        return ( center , radius )

    """
    param contour should be a list of lists.  The outer list should correspond to a closed-planar contour
    The inner lists are triples of y,x coordinates
    """
    def fill_slice_from_contour(self , z_idx , contour):
        for yi in range(self.array_sz[1]):
            y_mm = self.start_pos[1] + yi * self.vox_sz[1]
            for xi in range(self.array_sz[2]):
                x_mm = self.start_pos[2] + xi * self.vox_sz[2]
                self.data[z_idx,yi,xi] = float(utils.point_inside_polygon( (x_mm,y_mm) , contour ))

    def compute_dice(mask_other):
        return 0

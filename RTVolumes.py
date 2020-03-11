import gzip , struct , math , copy, itertools
import numpy as np
import scipy.ndimage as ndimage
import scipy.interpolate
from . import utils

class RTVolume:

    def __init__(self):
        self.array_sz = [0.,0.,0.] # z,y,x
        self.vox_sz = [0.,0.,0.]   # z,y,x
        self.start_pos = [0.,0.,0.] # z,y,x
        self.data = None

    def copy(self,vol_in):
        self.array_sz = copy.copy(vol_in.array_sz)
        self.vox_sz = copy.copy(vol_in.vox_sz)
        self.start_pos = copy.copy(vol_in.start_pos)
        self.data = copy.deepcopy(vol_in.data)

    def copy_metadata(self, vol_in):
        self.array_sz = copy.copy(vol_in.array_sz)
        self.vox_sz = copy.copy(vol_in.vox_sz)
        self.start_pos = copy.copy(vol_in.start_pos)
        
    def allocate(self):
        self.data = np.empty(self.array_sz , dtype=float)

    def load_from_Segana(self , file_path_params , file_path_data):
        # 
        # load parameters file
        # 
        # open
        f = open(file_path_params,"r")
        params = {}
        # grab number of voxels
        line = f.readline()
        data = line.split()
        self.array_sz = (int(data[2]), int(data[1]), int(data[0])) # z,y,x
        # grab voxel size in each dimension
        line = f.readline()
        data = line.split()
        self.vox_sz = (float(data[2]), float(data[1]), float(data[0])) # z,y,x
        # grab start positions
        line = f.readline()
        data = line.split()
        self.start_pos = (float(data[2]), float(data[1]), float(data[0])) # z,y,x
        # done
        f.close()
        # 
        # load binary data
        # 
        f = gzip.open(file_path_data,"rb")
        # self.data = np.array(struct.unpack('f'*self.array_sz[0]*self.array_sz[1]*self.array_sz[2],f.read())).reshape((self.array_sz[2],self.array_sz[1],self.array_sz[0]))
        self.data = np.array(struct.unpack('f'*self.array_sz[0]*self.array_sz[1]*self.array_sz[2],f.read())).reshape((self.array_sz[0],self.array_sz[1],self.array_sz[2]))
        # self.data = np.swapaxes(self.data,0,2)
        f.close()

    def idx_to_mm(self , points_idx):
        """ 
        Convert the supplied data points (indices) into positions in mm
        
        points_idx: a 3xN nparray of x,y,z points where x is the first row and z is the last.
        """
        points_mm = points_idx.astype(float) # will make a copy
        points_mm *= np.array([self.vox_sz]).T # pad and then transpose so it can broadcast
        points_mm += np.array([self.start_pos]).T
        return points_mm

    def mm_to_idx(self , points_mm):
        """ 
        Convert the supplied data points (in mm) into floating point indices.
        
        points_mm: a 3xN nparray of x,y,z points where x is the first row and z is the last.
        """
        points_idx = points_mm.copy()
        points_idx -= np.array([self.start_pos]).T
        points_idx /= np.array([self.vox_sz]).T
        return points_idx

    def downsample_planes(self , num_vox):
        y_scale = float(num_vox) / float(self.array_sz[1])
        x_scale = float(num_vox) / float(self.array_sz[2])
        self.data = ndimage.zoom( self.data ,
                                  (1.0,x_scale,y_scale))
        self.array_sz[1] = num_vox
        self.array_sz[2] = num_vox
        self.vox_sz[1] *= (1./y_scale)
        self.vox_sz[2] *= (1./x_scale)

    def apply_bounding_sphere(self , center , radius , mask_val):

        x_positions = [self.start_pos[2] + self.vox_sz[2] * float(xi) for xi in range(self.array_sz[2])]
        y_positions = [self.start_pos[1] + self.vox_sz[1] * float(yi) for yi in range(self.array_sz[1])]
        z_positions = [self.start_pos[0] + self.vox_sz[0] * float(zi) for zi in range(self.array_sz[0])]
        distances = [np.linalg.norm(np.array([mm[0],mm[1],mm[2]]) - np.array(center)) for mm in itertools.product( z_positions , y_positions , x_positions )]
        mask = distances > radius
        self.data[mask] = mask_val

    def sample_at_points( self , pts_idx_in ):
        # create positions where dose is currently found
        # z_mm = np.arange( self.start_pos[0] , self.start_pos[0] + self.array_sz[0]*self.vox_sz[0] , step=self.vox_sz[0] )
        # y_mm = np.arange( self.start_pos[1] , self.start_pos[1] + self.array_sz[1]*self.vox_sz[1] , step=self.vox_sz[1] )
        # x_mm = np.arange( self.start_pos[2] , self.start_pos[2] + self.array_sz[2]*self.vox_sz[2] , step=self.vox_sz[2] )


        # # convert dose array points to a mesh grid
        # X_grid,Y_grid,Z_grid = np.meshgrid( x_mm , y_mm , z_mm )

        # # convert sample positions to a mesh grid
        # sample_pts = np.meshgrid( pts_mm_in[0,:] , pts_mm_in[1,:] , pts_mm_in[2,:] )
        
        # # interpolate
        # return scipy.interpolate.interpn( (X_grid,Y_grid,Z_grid) , self.data , sample_pts , method="linear" )

        # # interpolate
        # return scipy.interpolate.interpn( (x_mm,y_mm,z_mm) , self.data , pts_mm_in.T , method="linear" )

        z_idx = np.linspace(0,255,256)
        y_idx = np.linspace(0,255,256)
        x_idx = np.linspace(0,255,256)

        return scipy.interpolate.interpn( (x_idx,y_idx,z_idx) , self.data , pts_idx_in.T , method="linear" )

class Mask(RTVolume):

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

class CTdata(RTVolume):

    def load_from_DICOM(self, dir_path):
        # load all images from directory path
        CT_images = []
        for root , dirs, files in os.walk(dir_path):
            for file in files:
                blah,ext = os.path.splitext(os.path.join(root,file))
                if ext == ".dcm":
                    dicom_content = pydicom.dcmread(os.path.join(root,file))
                    num_rows = int(dicom_content[0x0028 , 0x0010].value)
                    num_cols = int(dicom_content[0x0028 , 0x0011].value)
                    pixel_spacing = [float(i) for i in dicom_content[0x0028 , 0x0030].value]
                    patient_pos = [float(i) for i in dicom_content[0x0020 , 0x0032].value]
                    pixel_data = dicom_content.pixel_array.astype(float)
                    CT_images += [{"pos":patient_pos,
                                   "data":pixel_data}]
        # sort the CT images according to the patient position
        CT_images = sorted(CT_images , key=lambda ct: ct["pos"][2])
        # fill in data members
        self.array_sz = [len(CT_images),num_rows,num_cols] # z,y,x
        self.vox_sz = [CT_images[1]["pos"][2] - CT_images[0]["pos"][2],pixel_spacing[1],pixel_spacing[0]]
        self.start_pos = [CT_images[0]["pos"][2] , CT_images[0]["pos"][1] , CT_images[0]["pos"][0]]
        self.data = np.stack([cti["data"] for cti in CT_images])


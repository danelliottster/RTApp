import gzip , struct , math , copy, itertools
import numpy as np
import scipy.ndimage as ndimage
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

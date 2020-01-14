import gzip , struct , math , copy , os
import numpy as np
from . import utils
from . import RTVolume
import pydicom

class CTdata(RTVolume):

    # def __init__(self):
    #     RTVolume.__init__(self)

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


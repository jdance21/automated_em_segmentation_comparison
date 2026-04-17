## This the code that was made to calculate the packing fractions for the predictions from Segment Anything for Microscopy (micro_sam)
## Similar process can be done for ground truth packing fractions from manual segmentations performed by Daniel Girard



import nrrd
import tiffile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


##automated segmentation which will be the prediction
auto_seg = tiffile.imread("M1D1S1_auto_segmentation.tif")

##convert files to binary map where 1 = segmentation, 0 = empty
auto_bin = (auto_seg > 0).astype(np.uint8)

#cropping the picture but then the dimensions don't match, AH
h = auto_bin.shape[-2] #image height
crop_row = int(0.83 * h) #keep top 83% 
auto_crop = auto_bin[..., :crop_row, :]

fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(auto_crop, cmap="gray")

ax.set_title("Automated Binary Segmentation")
ax.set_xlabel("X Pixels")
ax.set_ylabel("Y Pixels")
plt.show()

segmented = np.sum(auto_crop == 1)
print("segmented pixels: " , segmented)
background = np.sum(auto_crop == 0)
print("background pixels: " , background)
total = segmented + background 
print("total pixels: " , total)

f = segmented/total
print("packing fraction: ", f)

##save results into an Excel spreadsheet as floats
data = {"Metrics": ["Segmented Pixels", "Total Pixels", "f" ], 
"Values": [segmented, total, f],} 
df = pd.DataFrame(data)

##manual segmentations which will be the ground truths
manual_seg, manual_header = nrrd.read("M1D1S1_intra-axonal_myelin_gt_map.nrrd")

##fix manual_seg shape to match auto_seg size
    ##remove (1) dimension
manual_seg = np.squeeze(manual_seg) 
    ##transpose the shape to match auto_seg 
manual_seg = manual_seg.T            

##convert files to binary map where 1 = segmentation, 0 = empty
manual_bin = (manual_seg > 0).astype(np.uint8)

#cropping the picture but then the dimensions don't match, AH
h = manual_bin.shape[-2]  #image height
crop_row = int(0.83 * h)   #keep top 83% 
manual_crop = manual_bin[..., :crop_row, :]

fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(manual_crop, cmap="gray")
ax.set_title("Automated Binary Segmentation")
ax.set_xlabel("X Pixels")
ax.set_ylabel("Y Pixels")
plt.show()

segmented = np.sum(manual_crop == 1)
print("segmented pixels: " , segmented)
background = np.sum(manual_crop == 0)
print("background pixels: " , background)
total = segmented + background 
print("total pixels: " , total)
f = segmented/total
print("packing fraction: ", f)

##save results into an Excel spreadsheet as floats
data = {"Metrics": ["Segmented Pixels", "Total Pixels", "f" ], 
"Values": [segmented, total, f],} 
df = pd.DataFrame(data)

##save to Excel
output_filename = "M1D1S8_intra-axonal_myelin_f.xlsx"
df.to_excel(output_filename, index=False)

print(f"Metrics saved to {output_filename}")



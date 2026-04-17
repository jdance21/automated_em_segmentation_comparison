## This is the code that was made to calculate the Dice similarity coefficient, precision and accuracy when comparing the predicitions to the ground truths
## The preidictions are from Segment Anything for Microscopy (micro_sam), ground truths are manual segmentations by Daniel Girard


import nrrd
import tiffile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


##manual segmentations which will be the ground truths
manual_seg, manual_header = nrrd.read("M1D1S8_intra-axonal_myelin_gt_map.nrrd")

##automated segmentation which will be the prediction 
auto_seg = tiffile.imread("M1D1S8_auto_segmentation.tif")

##fix manual_seg shape to match auto_seg size
    ##remove (1) dimension
manual_seg = np.squeeze(manual_seg) 
    ##transpose the shape to match auto_seg 
manual_seg = manual_seg.T            


##see if files are same size
if manual_seg.shape != auto_seg.shape:
    raise ValueError("Shape still does not match! Fix it dummy!")


##convert files to binary map where 1 = segmentation, 0 = empty
    #.astype(np.uint8) says that if manual_seg > 0, then assign it to 1
    #.astype(np.uint8) says that if manual_seg > 0, the assign it to 0
manual_bin = (manual_seg > 0).astype(np.uint8)
auto_bin = (auto_seg > 0).astype(np.uint8)

#cropping the picture
h = manual_bin.shape[-2]  #image height
crop_row = int(0.83 * h)   
manual_crop = manual_bin[..., :crop_row, :]
auto_crop = auto_bin[..., :crop_row, :]

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(manual_crop, cmap="gray")
axes[0].set_title("Manual Binary Segmentation")
plt.imsave("binary_manual_image.png", manual_crop, cmap="gray")
axes[1].imshow(auto_crop, cmap="gray")
axes[1].set_title("Automated Binary Segmentation")
plt.imsave("binary_auto_image.png", auto_crop, cmap="gray")
plt.show()

##find dice similarity coefficient, precision, and accuracy 
dice = []
precision = []
accuracy = []

for i in range(manual_crop.shape[0]): 
    TP = np.sum((manual_crop == 1) & (auto_crop == 1))
    FP = np.sum((manual_crop == 0) & (auto_crop == 1))
    FN = np.sum((manual_crop == 1) & (auto_crop == 0))
    TN = np.sum((manual_crop == 0) & (auto_crop == 0))

#DSC
if (2*TP + FP + FN) > 0:
    dice = (2 * TP) / (2 * TP + FP + FN)
else:
    dice = np.nan

#precision
if (TP + FP) > 0:
    precision = TP / (TP + FP)
else:
    precision = np.nan

#accuracy 
if (TP + FP + TN + FN) > 0:
    accuracy = (TP + TN) / (TP + FP + TN + FN)
else:
    accuracy = np.nan

print(f"Dice value:      {dice:.5f}")
print(f"Precision value: {precision:.5f}")
print(f"Accuracy value:  {accuracy:.5f}")

##save results into an Excel spreadsheet as floats
data = {
    "Metric": ["Dice", "Precision", "Accuracy"],
    "Mean": [dice, precision, accuracy],
} 

print(type(precision))
print(type(dice))
print(type(accuracy))

df = pd.DataFrame(data)

##save to Excel
output_filename = "M1D1S8_0.75_LM_other-cells_comparison.xlsx"
df.to_excel(output_filename, index=False)

print(f"Metrics saved to {output_filename}")


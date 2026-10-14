# ABBA - ABBA Start

Menu: `Plugins > BIOP > Atlas > ABBA - ABBA Start`  
Class: `ch.epfl.biop.atlas.aligner.gui.bdv.ABBABdvStartCommand`

Starts ABBA in a BigDataViewer window, with an atlas sliced along the chosen orientation. Slices are then imported, positioned along the slicing axis and registered to the atlas.

## Inputs

- `ba` (Atlas) **Atlas**
  Atlas to register the slices to, as output by an atlas opening command.
- `x_axis` (String) **X axis (sections, left to right)**, one of: `AP (Anterior-Posterior)`, `PA (Posterior-Anterior)`, `SI (Superior-Inferior)`, `IS (Inferior-Superior)`, `RL (Right-Left)`, `LR (Left-Right)`
  Anatomical direction of the horizontal axis of the displayed sections, from left to right on screen. Coronal: RL, sagittal: AP, horizontal: LR.
- `y_axis` (String) **Y axis (sections, top to bottom)**, one of: `AP (Anterior-Posterior)`, `PA (Posterior-Anterior)`, `SI (Superior-Inferior)`, `IS (Inferior-Superior)`, `RL (Right-Left)`, `LR (Left-Right)`
  Anatomical direction of the vertical axis of the displayed sections, from top to bottom on screen. Coronal: SI, sagittal: SI, horizontal: AP.
- `z_axis` (String) **Z axis (slicing axis)**, one of: `AP (Anterior-Posterior)`, `PA (Posterior-Anterior)`, `SI (Superior-Inferior)`, `IS (Inferior-Superior)`, `RL (Right-Left)`, `LR (Left-Right)`
  Anatomical direction of the slicing axis, along which the sections are positioned, in increasing position. Coronal: AP, sagittal: LR, horizontal: SI. The three axes must be different.

## Outputs

- `mp` (MultiSlicePositioner): The ABBA session (MultiSlicePositioner) shown in the window, used by the other ABBA commands.
- `view` (BdvMultislicePositionerView): The ABBA BigDataViewer view; its aligner (MultiSlicePositioner) is used by the other ABBA commands.


# ABBA - ABBA Start (alpha)

Menu: `Plugins > BIOP > Atlas > ABBA - ABBA Start (alpha)`  
Class: `ch.epfl.biop.atlas.aligner.gui.bdv.ABBABiopBdvStartCommand`

Experimental: starts ABBA in a BigDataViewer window with alpha blending of the sources, and optionally a white background, with an atlas sliced along the chosen orientation.

## Inputs

- `ba` (Atlas) **Atlas**
  Atlas to register the slices to, as output by an atlas opening command.
- `white_background` (boolean) **White background**, default `false`
  If checked, the viewer has a white background and a light theme, convenient for brightfield images.
- `x_axis` (String) **X axis (sections, left to right)**, one of: `AP (Anterior-Posterior)`, `PA (Posterior-Anterior)`, `SI (Superior-Inferior)`, `IS (Inferior-Superior)`, `RL (Right-Left)`, `LR (Left-Right)`
  Anatomical direction of the horizontal axis of the displayed sections, from left to right on screen. Coronal: RL, sagittal: AP, horizontal: LR.
- `y_axis` (String) **Y axis (sections, top to bottom)**, one of: `AP (Anterior-Posterior)`, `PA (Posterior-Anterior)`, `SI (Superior-Inferior)`, `IS (Inferior-Superior)`, `RL (Right-Left)`, `LR (Left-Right)`
  Anatomical direction of the vertical axis of the displayed sections, from top to bottom on screen. Coronal: SI, sagittal: SI, horizontal: AP.
- `z_axis` (String) **Z axis (slicing axis)**, one of: `AP (Anterior-Posterior)`, `PA (Posterior-Anterior)`, `SI (Superior-Inferior)`, `IS (Inferior-Superior)`, `RL (Right-Left)`, `LR (Left-Right)`
  Anatomical direction of the slicing axis, along which the sections are positioned, in increasing position. Coronal: AP, sagittal: LR, horizontal: SI. The three axes must be different.

## Outputs

- `view` (BdvMultislicePositionerView): The ABBA BigDataViewer view; its aligner (MultiSlicePositioner) is used by the other ABBA commands.


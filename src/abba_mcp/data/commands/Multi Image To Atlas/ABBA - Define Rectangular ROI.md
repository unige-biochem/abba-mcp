# ABBA - Define Rectangular ROI

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > ABBA - Define Rectangular ROI`  
Class: `ch.epfl.biop.atlas.aligner.gui.bdv.card.SliceDefineROICommand`

Defines the rectangular region of interest (ROI) of the sections: registrations only consider this region, and exports to images are cropped to it. It applies to all slices.

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `view` (BdvMultislicePositionerView)
- `x_mm` (Double) **X (mm)**
  X coordinate of the top left corner of the region, in mm. The full atlas section is centered on 0.
- `y_mm` (Double) **Y (mm)**
  Y coordinate of the top left corner of the region, in mm. The full atlas section is centered on 0.
- `width_mm` (Double) **Width (mm)**
  Width of the region, in mm.
- `height_mm` (Double) **Height (mm)**
  Height of the region, in mm.


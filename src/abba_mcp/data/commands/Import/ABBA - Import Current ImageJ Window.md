# ABBA - Import Current ImageJ Window

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Import > ABBA - Import Current ImageJ Window`  
Class: `ch.epfl.biop.atlas.aligner.command.ImportSliceFromImagePlusCommand`

Imports an image opened in ImageJ as a single slice, all channels included. The image should be calibrated (pixel size).

## Inputs

- `image` (ImagePlus) **Image**
  ImageJ image to import; by default the current image.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slice_position_mm` (double) **Slice position (mm)**, default `0.0`
  Initial position of the slice along the atlas slicing axis, in mm, as the Z shown in the slice information (0 = front of the atlas).


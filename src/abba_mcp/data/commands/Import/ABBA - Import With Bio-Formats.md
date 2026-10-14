# ABBA - Import With Bio-Formats

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Import > ABBA - Import With Bio-Formats`  
Class: `ch.epfl.biop.atlas.aligner.command.ImportSlicesFromFilesCommand`

Imports images from Bio-Formats compatible files (vsi, czi, ome.tiff, lif...) as slices. Each image series of each file becomes one slice, all channels included. The imported slices are selected.

## Inputs

- `datasetname` (String) **Dataset name**
  Name of the dataset grouping the imported images in the BigDataViewer-Playground source tree.
- `files` (File[]) **Files to import**
  Image files to open with Bio-Formats. Files should have a pixel size calibration.
- `first_slice_position_mm` (double) **Position of the first slice (mm)**, default `0.0`
  Initial position of the first imported slice along the atlas slicing axis, in mm, as the Z shown in the slice information (0 = front of the atlas). Positions can be adjusted later, for instance with DeepSlice.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slice_spacing_mm` (double) **Spacing between slices (mm)**, default `0.0`
  Distance between consecutive imported slices along the slicing axis, in mm. Use a negative value to reverse their order.
- `split_rgb_channels` (boolean) **Split RGB channels**, default `false`
  If checked, RGB images are split into three channels (red, green, blue); otherwise they are kept as a single RGB channel.


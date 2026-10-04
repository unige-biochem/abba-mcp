# ABBA - Export Atlas Coordinates of Original Slices to ImageJ

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Atlas Coordinates of Original Slices to ImageJ`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportDeformationFieldToImageJCommand`

For each selected slice, exports a 3-channel (x, y, z) 32-bit ImageJ image with the same pixels as the original unregistered slice image: each pixel holds its atlas coordinates, in mm. Waits for the registrations of the slices to be done.

## Inputs

- `downsampling` (int) **Additional downsampling factor**, default `1`
  Integer factor to further downsample the exported image, on top of the resolution level. 1 = no downsampling.
- `max_number_of_iterations` (int) **Max iterations for transform inversion**, default `200`
  Maximum number of iterations used to numerically invert non-linear (spline) registrations. Increase it if the inversion does not converge. Default 200.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `resolution_level` (int) **Resolution level**, default `0`
  Resolution level of the original image the exported image matches: 0 = full resolution, 1 = first downscaled level, etc. Must exist in the slice files.

## Outputs

- `images` (ImagePlus[]): One coordinates image per selected slice.


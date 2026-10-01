# ABBA - Export Original Slices to ImageJ

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Original Slices to ImageJ`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportSlicesOriginalDataToImageJCommand`

Opens in ImageJ the original, unregistered image of each selected slice, at the chosen resolution level. Fails for images larger than 2 billion pixels (use a lower resolution level). Useful together with the regions exported to the ROI Manager.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `resolution_level` (int) **Resolution level**, default `0`
  0 = full resolution, 1 = first downscaled level, etc. Must exist in all selected slices.
- `slice_channels_csv` (String) **Slice channels**, default `*`
  0-based indices of the slice channels to export, comma separated (e.g. '0,2'), or '*' for all channels.
- `verbose` (boolean) **Verbose**, default `false`
  If checked, logs the progress of the image loading.

## Outputs

- `images` (ImagePlus[]): One ImageJ image per selected slice.


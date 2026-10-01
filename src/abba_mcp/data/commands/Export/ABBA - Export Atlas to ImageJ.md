# ABBA - Export Atlas to ImageJ

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Atlas to ImageJ`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportAtlasToImageJCommand`

Exports the atlas section at the position of each selected slice as an ImageJ image, one plane per slice, within the current region of interest. Same geometry as 'Export Registered Slices to ImageJ' with the same pixel size, so both images can be overlaid.

## Inputs

- `atlas_channels_csv` (String) **Atlas channels**, default `*`
  0-based indices of the atlas channels to export, comma separated (e.g. '0,1'), or '*' for all channels. Depending on the atlas, channels include anatomical images, region borders, atlas coordinates, a left/right indicator and region labels.
- `image_name` (String) **Image name**, default `Atlas`
  Title of the exported ImageJ image.
- `interpolate` (boolean) **Interpolate**, default `false`
  If checked, pixels are linearly interpolated when resampled; otherwise the nearest pixel is used (keep it unchecked for label channels).
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `pixel_size_um` (double) **Pixel size (micrometers)**, default `20.0`
  Pixel size of the exported image.

## Outputs

- `image` (ImagePlus): Exported atlas image: one channel per atlas channel, one plane per selected slice.


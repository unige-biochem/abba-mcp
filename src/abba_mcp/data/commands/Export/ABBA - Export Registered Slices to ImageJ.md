# ABBA - Export Registered Slices to ImageJ

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Registered Slices to ImageJ`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportSlicesToImageJCommand`

Exports the registered (deformed) selected slices as an ImageJ image, one plane per slice, resampled at the given pixel size within the current region of interest, optionally with the atlas regions as overlay. Same geometry as 'Export Atlas to ImageJ'.

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `pixel_size_um` (double) **Pixel size (micrometers)**
  Pixel size of the exported image.
- `slice_channels_csv` (String) **Slice channels**
  0-based indices of the slice channels to export, comma separated (e.g. '0,2'), or '*' for all channels.
- `add_regions_overlay` (boolean) **Add atlas regions overlay**
  If checked, the atlas regions of each slice are added as an overlay of ROIs.
- `naming_choice` (String) **ROI naming**
  Atlas ontology property used to name each region ROI of the overlay, for instance its acronym, name or id. The available choices depend on the atlas. Ignored without overlay.
- `image_name` (String) **Image name**
  Title of the exported ImageJ image.
- `interpolate` (boolean) **Interpolate**
  If checked, pixels are linearly interpolated when resampled; otherwise the nearest pixel is used.

## Outputs

- `image` (ImagePlus)


# ABBA - Snapshot

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Inspect > ABBA - Snapshot`  
Class: `ch.epfl.biop.atlas.aligner.command.SnapshotCommand`

Renders slices with the atlas region borders at their current registration, independently of the window: a header describes each slice and rulers give coordinates in mm. Several slices are tiled. Region labels are the atlas at the slice position, not an observation: after an import that position is a placeholder (the header says 'reg=0'). Hide borders and labels to look at the tissue alone.

## Inputs

- `atlas_channel` (int) **Atlas channel**, default `-1`
  Index of an atlas channel blended with the slice, -1 for none.
- `columns` (int) **Columns**, default `0`
  Tiles per row when several slices are rendered, 0 for automatic.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session to render.
- `pixel_size_mm` (double) **Pixel size (mm)**, default `0.025`
  Pixel size of the rendered image; smaller is sharper and slower.
- `show_region_borders` (boolean) **Show region borders**, default `true`
- `show_region_labels` (boolean) **Show region labels**, default `true`
- `slices_csv` (String) **Slices**, optional
  0-based indices of the slices along the slicing axis, comma separated (e.g. '0,3'), '*' for all slices, or empty for the selected slices. Indices follow the slice order and change when a slice moves.

## Outputs

- `snapshot` (ImagePlus)


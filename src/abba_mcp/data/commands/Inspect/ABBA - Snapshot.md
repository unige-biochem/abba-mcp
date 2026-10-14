# ABBA - Snapshot

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Inspect > ABBA - Snapshot`  
Class: `ch.epfl.biop.atlas.aligner.command.SnapshotCommand`

Renders slices with the atlas region borders at their current registration, or an earlier one, independently of the window: a header describes each slice and rulers give coordinates in mm. Several slices are tiled. Region labels are the atlas at the slice position, not an observation: after an import that position is a placeholder (the header says 'reg=0'). Hide borders and labels to look at the tissue alone.

## Inputs

- `atlas_channel` (int) **Atlas channel**, default `-1`
  Index of an atlas channel blended with the slice, -1 for none ('atlas_channels' in 'ABBA - Get State' lists them in index order).
- `columns` (int) **Columns**, default `0`
  Tiles per row when several slices are rendered, 0 for automatic.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session to render.
- `pixel_size_mm` (double) **Pixel size (mm)**, default `0.025`
  Pixel size of the rendered image; smaller is sharper and slower.
- `region_mm` (String) **Region (mm)**, optional
  Rendered region 'x,y,width,height' in mm, x and y being its top left corner as read on the rulers (e.g. '-1,0.5,2,2' for a 2 mm square). Empty for the whole region of interest. With a small region, lower the pixel size to see details.
- `registration_step_back` (int) **Registration step back**, default `0`
  Renders the slices as they were this many registrations ago, 0 for their current registration (as 'View Previous' in the window). The header then says 'reg=shown/total', e.g. 'reg=2/4'; a slice with fewer registrations is rendered unregistered. Only the registrations are undone: the slice keeps its current position along the slicing axis.
- `show_region_borders` (boolean) **Show region borders**, default `true`
- `show_region_labels` (boolean) **Show region labels**, default `true`
- `slice_channels_csv` (String) **Slice channels**, default `*`
  0-based indices of the slice channels to render, comma separated (e.g. '0' for the first channel alone), or '*' for all channels. Each channel is rendered with its current display settings.
- `slices_csv` (String) **Slices**, optional
  0-based indices of the slices along the slicing axis, comma separated (e.g. '0,3'), '*' for all slices, or empty for the selected slices. Indices follow the slice order and change when a slice moves.

## Outputs

- `regions` (String): With region labels: each labelled region as 'acronym: full name', one per line, from the atlas ontology.
- `snapshot` (ImagePlus)


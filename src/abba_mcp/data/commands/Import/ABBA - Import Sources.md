# ABBA - Import Sources

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Import > ABBA - Import Sources`  
Class: `ch.epfl.biop.atlas.aligner.command.ImportSliceFromSourcesCommand`

Imports BigDataViewer-Playground sources as a single slice: each source becomes one channel of the slice.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slice_position_mm` (double) **Slice position (mm)**, default `0.0`
  Initial position of the slice along the atlas slicing axis, in mm, as the Z shown in the slice information (0 = front of the atlas).
- `sources` (SourceAndConverter[]) **Sources (channels)**
  Sources forming the slice, one per channel, in channel order. Their calibration should be in mm.


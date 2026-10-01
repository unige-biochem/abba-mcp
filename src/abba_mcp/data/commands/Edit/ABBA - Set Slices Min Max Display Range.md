# ABBA - Set Slices Min Max Display Range

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Set Slices Min Max Display Range`  
Class: `ch.epfl.biop.atlas.aligner.command.SetSlicesDisplayRangeCommand`

Sets the display range (min and max displayed values) of channels of the selected slices. Besides the display, it changes the images sent to DeepSlice: avoid saturated images.

## Inputs

- `display_max` (double) **Display max**, default `0.0`
  Pixel value displayed at full brightness; higher values are saturated.
- `display_min` (double) **Display min**, default `0.0`
  Pixel value displayed as black.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slice_channels_csv` (String) **Channels**, default `*`
  0-based indices of the channels to adjust, comma separated (e.g. '0,2'), or '*' for all channels. Channels missing in a slice are skipped.


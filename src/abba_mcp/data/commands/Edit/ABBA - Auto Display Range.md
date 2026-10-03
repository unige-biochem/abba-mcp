# ABBA - Auto Display Range

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Auto Display Range`  
Class: `ch.epfl.biop.atlas.aligner.command.AutoDisplayRangeCommand`

Sets the display range of channels of the selected slices from percentiles of their pixel values, measured on a downsampled resolution level. Besides the display, it changes the images sent to DeepSlice, which works best without saturation: run it before DeepSlice.

## Inputs

- `high_percentile` (double) **High percentile**, default `99.9`
  Percentile of the pixel values displayed at full brightness: 99.9 saturates 0.1% of the pixels.
- `low_percentile` (double) **Low percentile**, default `0.1`
  Percentile of the pixel values displayed as black.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `same_range_for_all_slices` (boolean) **Same range for all slices**, default `true`
  One range per channel, measured on all the selected slices together, so that slices look alike; otherwise one range per slice and channel.
- `slice_channels_csv` (String) **Channels**, default `*`
  0-based indices of the channels to adjust, comma separated (e.g. '0,2'), or '*' for all channels. Channels missing in a slice, and RGB channels, are skipped.

## Outputs

- `display_ranges` (String): The ranges set: per channel, or per slice and channel.


# ABBA - Get State

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Inspect > ABBA - Get State`  
Class: `ch.epfl.biop.atlas.aligner.command.GetStateCommand`

Returns the state of the session as JSON, once the queued work is done. Compact by default: the atlas, its channels in index order, the slicing angles, the region of interest, and per slice its index, name, position 'z_mm' (as displayed), selection, key slice flag, channel names and registrations. With 'full': the content of a state file instead, plus per slice its index, name, channels, selection and position in both conventions ('z_mm' as displayed, 'slicing_axis_position' as stored), long transforms elided.

## Inputs

- `full` (boolean) **Full state**, default `false`
  Returns the full state (every action, with its transforms) instead of the compact summary.
- `max_string_length` (int) **Max string length**, default `200`
  With 'full': longer strings, like spline transforms, are elided; 0 keeps them all.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session to read.
- `slices_csv` (String) **Slices**, default `*`, optional
  0-based indices of the slices along the slicing axis, comma separated (e.g. '0,3'), '*' for all slices, or empty for the selected slices. Indices follow the slice order and change when a slice moves.

## Outputs

- `state` (String): The state, as JSON.


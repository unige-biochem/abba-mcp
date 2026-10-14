# ABBA - Get State

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Inspect > ABBA - Get State`  
Class: `ch.epfl.biop.atlas.aligner.command.GetStateCommand`

Returns the state of the session as JSON, once the queued work is done or after 'timeout_s' seconds. Compact by default: 'pending_actions', the number of queued actions not done yet - above 0, positions and registrations are not final: call 'ABBA - Wait' -, the last 'failures' of the session (10 at most, one line each), the atlas, its channels in index order, the slicing angles, the region of interest, and per slice its index, name, position 'z_mm' (as displayed), 'thickness_mm', selection, key slice flag, channel names, registrations and 'pending' actions if any. With 'full': the content of a state file instead, plus per slice its index, name, channels, selection and position in both conventions ('z_mm' as displayed, 'slicing_axis_position' as stored), long transforms elided, and 'pending_actions' and 'failures' as well.

## Inputs

- `full` (boolean) **Full state**, default `false`
  Returns the full state (every action, with its transforms) instead of the compact summary.
- `max_string_length` (int) **Max string length**, default `200`
  With 'full': longer strings, like spline transforms, are elided; 0 keeps them all.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session to read.
- `slices_csv` (String) **Slices**, default `*`, optional
  0-based indices of the slices along the slicing axis, comma separated (e.g. '0,3'), '*' for all slices, or empty for the selected slices. Indices follow the slice order and change when a slice moves.
- `timeout_s` (double) **Timeout (s)**, default `20.0`
  Longest wait for the queued actions, in seconds; the state is returned anyway after it.

## Outputs

- `state` (String): The state, as JSON.


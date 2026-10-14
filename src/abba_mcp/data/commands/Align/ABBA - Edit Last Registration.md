# ABBA - Edit Last Registration

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - Edit Last Registration`  
Class: `ch.epfl.biop.atlas.aligner.command.RegisterSlicesEditLastCommand`

Manually edits the last registration of each selected slice, if it is editable: spline registrations (Elastix spline, BigWarp) open in BigWarp, affine registrations (Elastix affine, manual, DeepSlice) open in the affine editor.

## Inputs

- `atlas_channels_csv` (String) **Atlas channels displayed**, default `*`
  0-based indices of the atlas channels displayed in the editor, comma separated (e.g. '0,2'), or '*' for all channels. Ignored if the channels used by the registration are displayed.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `reuse_original_channels` (boolean) **Display the channels used by the registration**, default `false`
  If checked, the editor displays the channels used when the registration was made, and the two channel fields below are ignored.
- `slice_channels_csv` (String) **Slice channels displayed**, default `*`
  0-based indices of the slice channels displayed in the editor, comma separated (e.g. '0,2'), or '*' for all channels. Ignored if the channels used by the registration are displayed.


# ABBA - BigWarp Registration

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - BigWarp Registration`  
Class: `ch.epfl.biop.atlas.aligner.command.RegisterSlicesBigWarpCommand`

Manual in-plane non-linear registration of the selected slices: each slice is opened in BigWarp, one after the other, where landmarks are placed by hand. Selected channels are only used for display.

## Inputs

- `atlas_channels_csv` (String) **Atlas channels**
  0-based indices of the atlas channels to use, comma separated (e.g. '0,1'). '*' is not accepted. The channels in index order are 'atlas_channels' in 'ABBA - Get State', and in the atlas display card.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slice_channels_csv` (String) **Slice channels**
  0-based indices of the slice channels to use, comma separated (e.g. '0,1'). '*' is not accepted.


# ABBA - Manual Affine Registration

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - Manual Affine Registration`  
Class: `ch.epfl.biop.atlas.aligner.command.RegisterSlicesManualAffineCommand`

Manual in-plane affine registration: moves, rotates, scales and shears the selected slices with a gizmo, in a single dedicated window. Selected channels are only used for display. The result can be edited later.

## Inputs

- `atlas_channels_csv` (String) **Atlas channels**
  0-based indices of the atlas channels to use, comma separated (e.g. '0,1'). '*' is not accepted. The channels in index order are 'atlas_channels' in 'ABBA - Get State', and in the atlas display card.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slice_channels_csv` (String) **Slice channels**
  0-based indices of the slice channels to use, comma separated (e.g. '0,1'). '*' is not accepted.


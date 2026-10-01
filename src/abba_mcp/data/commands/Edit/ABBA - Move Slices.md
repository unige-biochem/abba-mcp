# ABBA - Move Slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Move Slices`  
Class: `ch.epfl.biop.atlas.aligner.command.MoveSlicesCommand`

Moves slices along the slicing axis to the given positions, as dragging them in the ABBA window does. Positions are in mm, in the displayed convention ('z_mm' in ABBA - Get State). One undo step. Slice indices change after a move: re-read the state.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slices_csv` (String) **Slices**
  0-based indices of the slices to move, comma separated (e.g. '0,3'), in the current order along the slicing axis.
- `z_mm_csv` (String) **Positions (mm)**
  New position of each slice along the slicing axis, in mm, comma separated, one per slice index (e.g. '6.2,6.6'). Displayed convention, as 'z_mm' in ABBA - Get State.


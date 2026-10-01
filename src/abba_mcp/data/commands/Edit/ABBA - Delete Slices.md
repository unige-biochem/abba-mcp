# ABBA - Delete Slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Delete Slices`  
Class: `ch.epfl.biop.atlas.aligner.command.DeleteSlicesCommand`

Removes slices from the session, as the delete action of the ABBA window does. No file is touched, and undo restores them. Slide scanner files often hold images that are not sections (label, overview, macro): check their names in the state before deleting.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slices_csv` (String) **Slices**, optional
  0-based indices of the slices along the slicing axis, comma separated (e.g. '0,3'), '*' for all slices, or empty for the selected slices. Indices follow the slice order and change when a slice moves.


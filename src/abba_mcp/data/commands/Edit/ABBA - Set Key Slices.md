# ABBA - Set Key Slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Set Key Slices`  
Class: `ch.epfl.biop.atlas.aligner.command.SetKeySlicesCommand`

Marks slices as key slices (or unmarks them). Key slices keep their position when ABBA - Distribute Slices spaces the others evenly: place 2 or 3 of them where you trust the position. One undo step.

## Inputs

- `key` (boolean) **Key slice**, default `true`
  Checked: mark as key slices. Unchecked: remove the mark.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slices_csv` (String) **Slices**, optional
  0-based indices of the slices along the slicing axis, comma separated (e.g. '0,3'), '*' for all slices, or empty for the selected slices. Indices follow the slice order and change when a slice moves.


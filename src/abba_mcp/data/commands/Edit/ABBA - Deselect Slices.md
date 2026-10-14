# ABBA - Deselect Slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Deselect Slices`  
Class: `ch.epfl.biop.atlas.aligner.command.SetSlicesDeselectedCommand`

Removes slices from the current selection, by index. Other slices keep their selection state.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slices_csv` (String) **Slice indices**, default `*`
  0-based indices of the slices, in the order along the slicing axis. '*' for all slices, comma separated values ('0,3'), inclusive ranges ('2:5'), ranges with a step ('0:2:10'). Negative indices count from the end: -1 is the last slice.


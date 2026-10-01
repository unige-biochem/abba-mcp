# ABBA - Select Slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Select Slices`  
Class: `ch.epfl.biop.atlas.aligner.command.SetSlicesSelectedCommand`

Adds slices to the current selection, by index. Already selected slices stay selected. Most commands act on the selected slices.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `slices_csv` (String) **Slice indices**, default `*`
  0-based indices of the slices, in the order along the slicing axis. '*' for all slices, comma separated values ('0,3'), inclusive ranges ('2:5'), ranges with a step ('0:2:10'). Negative indices count from the end: -1 is the last slice.


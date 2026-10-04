# ABBA - Distribute Slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Distribute Slices`  
Class: `ch.epfl.biop.atlas.aligner.command.DistributeSlicesCommand`

Spaces the selected slices evenly along the slicing axis, as 'Distribute Slices [D]' does in the ABBA window. The first and last selected slices and the key slices (ABBA - Set Key Slices) do not move; the slices between two of them are spaced evenly. Needs at least 3 selected slices. One undo step.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.


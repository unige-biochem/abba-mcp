# ABBA - Set Slices Thickness (fill gaps)

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Set Slices Thickness (fill gaps)`  
Class: `ch.epfl.biop.atlas.aligner.command.SetSlicesThicknessMatchNeighborsCommand`

Sets the thickness of each selected slice so that it extends halfway to its neighbors, leaving no gap between slices. It affects the 3D display (reconstructed brain) and the 3D resampled export, not the registrations.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.


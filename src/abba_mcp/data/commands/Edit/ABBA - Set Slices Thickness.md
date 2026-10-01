# ABBA - Set Slices Thickness

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Set Slices Thickness`  
Class: `ch.epfl.biop.atlas.aligner.command.SetSlicesThicknessCommand`

Sets the thickness of the selected slices along the slicing axis. It affects the 3D display (reconstructed brain) and the 3D resampled export, not the registrations.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `thickness_um` (double) **Slice thickness (micrometers)**, default `0.0`
  Thickness of each selected slice, centered on its position.


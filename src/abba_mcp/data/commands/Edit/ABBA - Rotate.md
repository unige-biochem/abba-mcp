# ABBA - Rotate

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Rotate`  
Class: `ch.epfl.biop.atlas.aligner.command.RotateSlicesCommand`

Rotates the selected slices around the center of the registration ROI. Z: in-plane rotation, clockwise on screen. X or Y: 180 or -180 degrees only (flip)

## Inputs

- `angle_degrees` (double) **Angle (degrees)**, default `0.0`
  Rotation angle. Around Z, positive is clockwise on screen.
- `axis_string` (String) **Rotation axis**, one of: `Z`, `Y`, `X`
  'Z': in-plane rotation, any angle. 'X' or 'Y': flips the section upside down or left-right, only 180 or -180 degrees are accepted.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.


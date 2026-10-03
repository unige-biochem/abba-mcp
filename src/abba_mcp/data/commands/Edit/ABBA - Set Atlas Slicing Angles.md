# ABBA - Set Atlas Slicing Angles

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Set Atlas Slicing Angles`  
Class: `ch.epfl.biop.atlas.aligner.command.SetAtlasSlicingAnglesCommand`

Sets the angles at which the atlas is sliced, for all slices of the session: the correction for a cutting plane that was not perfectly orthogonal. DeepSlice sets them when 'Adjust atlas slicing angle' is checked. Not undoable: note the current angles first (ABBA - Get State, slicing_angle_x_deg and slicing_angle_y_deg). 'ABBA - Adjust Slicing' is its interactive form.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `x_degrees` (double) **Rotation around X (degrees)**, default `0.0`
  Rotation of the slicing plane around the horizontal axis of the sections.
- `y_degrees` (double) **Rotation around Y (degrees)**, default `0.0`
  Rotation of the slicing plane around the vertical axis of the sections.

## Outputs

- `angles` (String): The angles now in use, in degrees.


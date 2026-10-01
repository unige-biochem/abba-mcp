# ABBA - Adjust Slicing

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > ABBA - Adjust Slicing`  
Class: `ch.epfl.biop.atlas.aligner.command.AtlasSlicingAdjusterCommand`

Tilts the atlas slicing plane to match the sectioning angle of the slices. The angles apply to all slices.

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `lockAngles` (Boolean) **Lock rotations**
  If checked, the angles cannot be changed, to avoid modifying them by mistake.
- `rotateX` (double) **X rotation (degrees)**
  Rotation of the slicing plane around the X axis of the sections (horizontal on screen).
- `rotateY` (double) **Y rotation (degrees)**
  Rotation of the slicing plane around the Y axis of the sections (vertical on screen).
- `reslicedAtlas` (ReslicedAtlas)


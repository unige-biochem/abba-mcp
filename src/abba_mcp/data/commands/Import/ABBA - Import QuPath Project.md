# ABBA - Import QuPath Project

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Import > ABBA - Import QuPath Project`  
Class: `ch.epfl.biop.atlas.aligner.command.ImportSlicesFromQuPathCommand`

Imports all images of a QuPath project as slices, one slice per project image, all channels included. Registrations can then be exported back to the QuPath project. Do not add or remove images in the QuPath project after the import.

## Inputs

- `first_slice_position_mm` (double) **Position of the first slice (mm)**, default `0.0`
  Initial position of the first imported slice along the atlas slicing axis, in mm, as the Z shown in the slice information (0 = front of the atlas). Positions can be adjusted later, for instance with DeepSlice.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `qupath_project` (File) **QuPath project file (.qpproj)**
  The project.qpproj file of the QuPath project to import.
- `slice_spacing_mm` (double) **Spacing between slices (mm)**, default `0.0`
  Distance between consecutive imported slices along the slicing axis, in mm. Use a negative value to reverse their order. Cannot be 0.


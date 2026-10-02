# ABBA - Export Slices To New QuPath Project

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Slices To New QuPath Project`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportSlicesToNewQuPathProjectCommand`

Creates a QuPath project (QuPath 0.7) containing the images of the selected slices, with their atlas regions and their registration (ABBA-RoiSet and ABBA-Transform files), which are imported in QuPath with the ABBA extension. Only slices opened from a single series of a 2D file with Bio-Formats can be exported, one slice per image; use 'ABBA - Export Registrations To QuPath Project' for slices imported from a QuPath project.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `project_folder` (File) **QuPath project folder**
  Folder of the new QuPath project. It must be empty or not exist yet.


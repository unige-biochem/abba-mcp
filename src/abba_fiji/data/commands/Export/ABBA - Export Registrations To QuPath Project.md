# ABBA - Export Registrations To QuPath Project

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Registrations To QuPath Project`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportRegistrationToQuPathCommand`

For each selected slice imported from a QuPath project, saves its atlas regions and its registration (ABBA-RoiSet and ABBA-Transform files) in the QuPath project folder of the image. They are then imported in QuPath with the ABBA extension. Slices not imported from a QuPath project are not exported: slices opened from files can be exported with 'ABBA - Export Slices To New QuPath Project'.

## Inputs

- `erase_previous_file` (boolean) **Overwrite previous export**, default `false`
  If checked, a previous ABBA export of the same image is replaced; otherwise an error is reported for this image.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.


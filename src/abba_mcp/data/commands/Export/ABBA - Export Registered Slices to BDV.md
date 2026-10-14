# ABBA - Export Registered Slices to BDV

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Registered Slices to BDV`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportSlicesToBDVCommand`

Shows the registered selected slices, placed in atlas coordinates, in a new BigDataViewer window. The sources are also added to the BigDataViewer-Playground source tree. Waits for all ABBA tasks to be done.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `tag` (String) **Tag**
  Text stored as the 'ABBA' metadata of each exported source, to identify them later in scripts.


# ABBA - Export Registered Slices to BDV Json Dataset (Experimental)

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Registered Slices to BDV Json Dataset (Experimental)`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportSlicesToBDVJsonDatasetCommand`

Very experimental: saves the registered selected slices, placed in atlas coordinates, as a BigDataViewer-Playground json file which references the original images. Waits for all ABBA tasks to be done.

## Inputs

- `file` (File) **Output file (.json)**
  Json file to create.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `tag` (String) **Tag**
  Text stored as the 'ABBA' metadata of each exported source, to identify them later in scripts.


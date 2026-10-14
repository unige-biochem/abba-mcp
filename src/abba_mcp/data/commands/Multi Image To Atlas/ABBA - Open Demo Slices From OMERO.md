# ABBA - Open Demo Slices From OMERO

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > ABBA - Open Demo Slices From OMERO`  
Class: `ch.epfl.biop.atlas.aligner.command.ImportDemoSlicesOMEROCommand`

Imports demo mouse brain sections streamed from the German BioImaging OMERO server (shared read-only demo account, no credentials needed), through a QuPath project downloaded from Zenodo. Requires an internet connection and the OMERO dependencies.

## Inputs

- `demo_dataset` (String) **Demo dataset**, one of: `25 sections`, `97 sections`
  '25 sections': a subset, faster to try ABBA. '97 sections': the full brain.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `project_directory` (File) **QuPath project folder (optional)**, optional
  Folder where the demo QuPath project is downloaded, to keep it and export registrations to it; created if missing. If empty, a temporary folder is used.


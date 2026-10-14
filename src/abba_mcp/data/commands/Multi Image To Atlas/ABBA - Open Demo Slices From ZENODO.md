# ABBA - Open Demo Slices From ZENODO

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > ABBA - Open Demo Slices From ZENODO`  
Class: `ch.epfl.biop.atlas.aligner.command.ImportDemoSlicesZENODOCommand`

Imports demo mouse brain sections from whole slide images (vsi) downloaded from Zenodo and cached locally (about 1 GB per slide). The label and overview images of each slide are imported as extra slices (their name does not contain '10x'). All slices are selected at the end.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `number_of_slides` (int) **Number of slides**, default `1`
  Number of slides to download, from 1 to 7, picked around the central slide. Each slide contains several sections.


# ABBA - Import QuickNII Project

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Import > ABBA - Import QuickNII Project`  
Class: `ch.epfl.biop.atlas.aligner.command.ImportSlicesFromQuickNIICommand`

Imports the images of a QuickNII series (JSON file, also produced by DeepSlice) as slices, together with their registration: slice positions, in-plane affine transforms and atlas slicing angle. The import is approximate: a single slicing angle (median of all slices) is applied to all slices.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `quicknii_project` (File) **QuickNII file (.json)**
  QuickNII series file, in JSON format. The images it references must be in the same folder.
- `split_rgb_channels` (boolean) **Split RGB channels**, default `false`
  If checked, RGB images are split into three channels (red, green, blue); otherwise they are kept as a single RGB channel.


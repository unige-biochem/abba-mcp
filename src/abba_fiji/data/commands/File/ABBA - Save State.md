# ABBA - Save State

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > File > ABBA - Save State`  
Class: `ch.epfl.biop.atlas.aligner.command.ABBAStateSaveCommand`

Saves the current ABBA session (slices, positions, registrations, atlas slicing angles) in a .abba file. Images are not copied: the file references the original image files. Existing files are not overwritten.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `state_file` (File) **State file (.abba)**
  File to create. The '.abba' extension is added if there is none. The file must not exist already.

## Outputs

- `success` (Boolean): True if the state was saved.


# ABBA - Load State

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > File > ABBA - Load State`  
Class: `ch.epfl.biop.atlas.aligner.command.ABBAStateLoadCommand`

Loads a saved ABBA state (.abba file): slices, their positions and registrations, and the atlas slicing angles. The slices are added to the current session. The image files must still be at the location where they were when the state was saved.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `state_file` (File) **State file (.abba)**
  ABBA state file to load. It must have been saved with the same atlas.

## Outputs

- `success` (Boolean): True if the state was loaded.


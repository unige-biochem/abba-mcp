# ABBA - Undo or Redo

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Undo or Redo`  
Class: `ch.epfl.biop.atlas.aligner.command.UndoCommand`

Undoes (or redoes) the last user actions of a session, as Ctrl+Z (Ctrl+Shift+Z) does in the ABBA window. One command can queue several actions: DeepSlice on n slices is n actions. The atlas slicing angles are not undone.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `steps` (int) **Steps**, default `1`
  Number of actions to undo; negative to redo.


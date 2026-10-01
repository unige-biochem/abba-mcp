# ABBA - Mirror Slices

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - Mirror Slices`  
Class: `ch.epfl.biop.atlas.aligner.command.MirrorDoCommand`

Turns hemi-sections into full sections, for instance before DeepSlice which needs full sections. The vertical midline of the atlas acts as a mirror: the half of each selected slice on the chosen side is kept, and its mirror image replaces the other half. Place the hemi-section against the atlas midline first. Undo with 'Un-Mirror Slices'.

## Inputs

- `mirror_side` (String) **Half to keep (as displayed)**, one of: `Left`, `Right`
  Side of the atlas midline, as displayed on screen, where the tissue is. 'Left': the left half is kept and mirrored onto the right half. 'Right': the right half is kept and mirrored onto the left half.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.


# ABBA - Copy and Apply Registration

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - Copy and Apply Registration`  
Class: `ch.epfl.biop.atlas.aligner.command.RegisterSlicesCopyAndApplyCommand`

Copies all registrations of a model slice and appends them, as they are (no new computation), to the registrations of each selected slice. The model slice itself is left unchanged.

## Inputs

- `model_slice_index` (int) **Model slice index**, default `0`
  0-based index of the slice whose registrations are copied, in the slice order along the slicing axis.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `skip_pre_transform` (boolean) **Skip the pre-transform**, default `false`
  If checked, the model slice pre-transform is not copied: the out-of-plane part of X or Y flips, and rotations made with older ABBA versions. In-plane edits are registrations and are always copied.


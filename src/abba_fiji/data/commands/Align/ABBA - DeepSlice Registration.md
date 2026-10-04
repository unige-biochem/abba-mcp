# ABBA - DeepSlice Registration

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - DeepSlice Registration`  
Class: `ch.epfl.biop.atlas.aligner.command.RegisterSlicesDeepSliceApposeCommand`

Runs DeepSlice (installed automatically in a local Python environment) on the selected slices: sets their position along the slicing axis, adds an in-plane affine registration and optionally adjusts the atlas slicing angle. The result depends on the slices display settings: avoid saturation.

## Inputs

- `allow_slicing_angle_change` (boolean) **Adjust atlas slicing angle**, default `true`
  If checked, the atlas slicing angles (X and Y rotations) are set to the median angle found by DeepSlice. This changes the slicing for all slices, not only the selected ones.
- `ensemble` (boolean) **Ensemble (average of several models, slower)**, default `false`
  If checked, DeepSlice averages the predictions of several models. Results may be better or not depending on the dataset: try both.
- `model` (String) **DeepSlice model**, one of: `mouse`, `rat`
  Species DeepSlice was trained on: 'mouse' or 'rat'. It should match the atlas.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `pixel_size_um` (double) **Pixel size sent to DeepSlice (micrometers)**
  Pixel size used to downsample the slices before sending them to DeepSlice. Defaults to 10.0 for mouse and 40.0 for rat; larger values are faster.
- `post_processing` (String) **Position post-processing**, one of: `Keep order`, `Keep order + ensure regular spacing`, `Keep order + set spacing (parameter below)`, `No post-processing`, `Keep current slice positions (in-plane registration only)`
  How the slice positions predicted by DeepSlice are corrected. 'Keep order': the current slice order is preserved. 'Keep order + ensure regular spacing': order preserved and slices evenly spaced, spacing estimated by DeepSlice. 'Keep order + set spacing (parameter below)': order preserved and slices evenly spaced with the spacing given below. 'No post-processing': raw DeepSlice positions, slices may be reordered. 'Keep current slice positions (in-plane registration only)': the slices are not moved, only registered in plane.
- `slice_channels_csv` (String) **Slice channels**, default `*`
  0-based indices of the slice channels sent to DeepSlice, comma separated (e.g. '0,2'), or '*' for all channels. Selected channels are merged into an RGB image with their current display settings (color and min/max).
- `slice_spacing_um` (double) **Slice spacing (micrometers)**, default `-1.0`
  Distance between consecutive slices. Only used with 'Keep order + set spacing (parameter below)'.


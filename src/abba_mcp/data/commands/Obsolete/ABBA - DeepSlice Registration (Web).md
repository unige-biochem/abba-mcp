# ABBA - DeepSlice Registration (Web)

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > (Obsolete) > ABBA - DeepSlice Registration (Web)`  
Class: `ch.epfl.biop.atlas.aligner.command.RegisterSlicesDeepSliceWebCommand`

Obsolete, use 'ABBA - DeepSlice Registration' instead. Registers the selected slices with the DeepSlice web interface: the downsampled slices are sent to the website by hand, and the result file is loaded back. Requires a graphical user interface.

## Inputs

- `allow_slicing_angle_change` (boolean) **Adjust atlas slicing angle**, default `true`
  If checked, the atlas slicing angles (X and Y rotations) are set to the median angle found by DeepSlice. This changes the slicing for all slices, not only the selected ones.
- `maintain_slices_order` (boolean) **Keep slice order**, default `false`
  If checked, slices keep their current order: slices swapped by DeepSlice are moved back.
- `model` (String) **DeepSlice model**, one of: `mouse`, `rat`
  Species DeepSlice was trained on: 'mouse' or 'rat'. It should match the atlas.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `pixel_size_um` (double) **Pixel size sent to DeepSlice (micrometers)**
  Pixel size used to downsample the slices before sending them to DeepSlice. Defaults to 10.0 for mouse and 40.0 for rat; larger values are faster.
- `slice_channels_csv` (String) **Slice channels**, default `*`
  0-based indices of the slice channels sent to DeepSlice, comma separated (e.g. '0,2'), or '*' for all channels. Selected channels are merged into an RGB image with their current display settings (color and min/max).


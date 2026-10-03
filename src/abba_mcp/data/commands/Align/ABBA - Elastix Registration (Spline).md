# ABBA - Elastix Registration (Spline)

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Align > ABBA - Elastix Registration (Spline)`  
Class: `ch.epfl.biop.atlas.aligner.command.RegisterSlicesElastixSplineCommand`

Automatic in-plane non-linear (B-spline) registration of the selected slices to the atlas with Elastix, restricted to the current region of interest. Usually run after an affine registration. Atlas and slice channels are paired in order and must be equal in number. The result can be edited in BigWarp.

## Inputs

- `atlas_channels_csv` (String) **Atlas channels**
  0-based indices of the atlas channels to use, comma separated (e.g. '0,1'). '*' is not accepted. The channels in index order are 'atlas_channels' in 'ABBA - Get State', and in the atlas display card.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `nb_control_points_x` (int) **Number of control points along X**, default `10`
  Size of the B-spline control point grid along X (minimum 2), the Y count follows the region of interest aspect ratio. More points allow more local deformations.
- `pixel_size_um` (double) **Registration pixel size (micrometers)**, default `20.0`
  Atlas and slices are resampled at this pixel size before being registered. Smaller is more precise but slower; 20 is a good start for a mouse brain.
- `show_imageplus_registration_result` (boolean) **Show registration images**, default `false`
  If checked, the resampled atlas and slice images sent to Elastix are displayed as ImageJ images (for debugging).
- `slice_channels_csv` (String) **Slice channels**
  0-based indices of the slice channels to use, comma separated (e.g. '0,1'). '*' is not accepted.


# ABBA - Raster and cache deformation field

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Raster and cache deformation field`  
Class: `ch.epfl.biop.atlas.aligner.command.RasterSlicesDeformationCommand`

Speeds up the display of the selected slices by computing their deformation field on a grid and interpolating it. Only useful after spline registrations. Experimental.

## Inputs

- `grid_spacing_um` (double) **Grid spacing (micrometers)**, default `150.0`
  Spacing of the grid on which the deformation is computed. Larger is faster but less accurate. Must be above the atlas resolution.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.


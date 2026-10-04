# ABBA - Export Resampled Slices as BDV Source ( experimental )

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Resampled Slices as BDV Source ( experimental )`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportResampledSlicesToBDVSourceCommand`

Experimental: fuses the registered selected slices into a 3D volume in atlas coordinates, resampled at the given voxel size and within the current region of interest, as multiresolution BigDataViewer sources (one per channel), computed lazily and cached.

## Inputs

- `block_size_x` (int) **Cache block size X (pixels)**, default `64`
  Size along X of the blocks computed and cached at once.
- `block_size_y` (int) **Cache block size Y (pixels)**, default `64`
  Size along Y of the blocks computed and cached at once.
- `block_size_z` (int) **Cache block size Z (pixels)**, default `4`
  Size along Z of the blocks computed and cached at once.
- `downsample_x` (int) **Downsampling between resolution levels X**, default `2`
  Factor along X between two consecutive resolution levels of the output.
- `downsample_y` (int) **Downsampling between resolution levels Y**, default `2`
  Factor along Y between two consecutive resolution levels of the output.
- `downsample_z` (int) **Downsampling between resolution levels Z**, default `1`
  Factor along Z between two consecutive resolution levels of the output.
- `image_name` (String) **Source name**, default `Untitled`
  Base name of the exported sources, '_ch<index>' is appended for each channel.
- `interpolate` (boolean) **Interpolate**, default `false`
  If checked, pixels are linearly interpolated when resampled; otherwise the nearest pixel is used.
- `margin_z_um` (double) **Z margin (micrometers)**, default `0.0`
  Extra space added before the first and after the last selected slice along the slicing axis.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `n_threads` (int) **Number of threads**, default `6`
  Number of threads used to compute the blocks.
- `resolution_levels` (int) **Number of resolution levels**, default `6`
  Number of resolution levels of the output sources, at least 1.
- `slice_channels_csv` (String) **Slice channels**, default `*`
  0-based indices of the slice channels to export, comma separated (e.g. '0,2'), or '*' for all channels.
- `voxel_size_x_um` (double) **Voxel size X (micrometers)**, default `20.0`
  Size of the output voxels along the X axis of the sections.
- `voxel_size_y_um` (double) **Voxel size Y (micrometers)**, default `20.0`
  Size of the output voxels along the Y axis of the sections.
- `voxel_size_z_um` (double) **Voxel size Z (micrometers)**, default `20.0`
  Size of the output voxels along the slicing axis.

## Outputs

- `fusedImages` (SourceAndConverter[]): One fused 3D source per exported channel.


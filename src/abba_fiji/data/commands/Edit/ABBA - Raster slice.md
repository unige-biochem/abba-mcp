# ABBA - Raster slice

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Raster slice`  
Class: `ch.epfl.biop.atlas.aligner.command.RasterSlicesCommand`

Speeds up the display of the selected slices by computing and caching their registered image at a fixed pixel size. The cached image has a lower resolution than the original image. Experimental.

## Inputs

- `interpolate` (boolean) **Interpolate**, default `false`
  If checked, pixels are linearly interpolated when resampled; otherwise the nearest pixel is used.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `pixel_size_um` (double) **Pixel size (micrometers)**, default `10.0`
  Pixel size of the cached images: larger is faster and uses less memory, but is blurrier.


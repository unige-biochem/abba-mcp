# ABBA - Export registered slices as QuickNII dataset

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export registered slices as QuickNII dataset`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportSlicesToQuickNIIDatasetCommand`

Exports the selected slices as a QuickNII dataset: registered (deformed) slice images resampled within the current region of interest, and a series JSON file with the position of each image in the atlas. The exported images already include all registrations. The folder is created if needed.

## Inputs

- `convert_to_8_bits` (boolean) **Convert to 8-bit**, default `true`
  If checked, images are converted to 8-bit before being saved.
- `convert_to_jpg` (boolean) **Save as JPEG**, default `true`
  If checked, images are saved as JPEG, the format QuickNII reads; a single channel is recommended. Otherwise they are saved as TIFF.
- `dataset_folder` (File) **Output folder**
  Folder where the images ('<prefix>_s000.jpg'...) and the '<prefix>.json' series file are written.
- `image_name` (String) **File name prefix**, default `Section`
  Prefix of the exported image files and name of the JSON series file.
- `interpolate` (boolean) **Interpolate**, default `false`
  If checked, pixels are linearly interpolated when resampled; otherwise the nearest pixel is used.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `pixel_size_um` (double) **Pixel size (micrometers)**, default `40.0`
  Pixel size at which the registered slices are resampled.
- `slice_channels_csv` (String) **Slice channels**, default `*`
  0-based indices of the slice channels to export, comma separated (e.g. '0,2'), or '*' for all channels.


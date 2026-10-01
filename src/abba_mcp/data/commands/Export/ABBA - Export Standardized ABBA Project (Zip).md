# ABBA - Export Standardized ABBA Project (Zip)

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Standardized ABBA Project (Zip)`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportStdZipStateCommand`

Creates a standardized, shareable zip of the current ABBA session: all slices downscaled to a given pixel size, their registrations, their deformation fields and metadata (atlas, slicing orientation, experiment information). The zip can be opened with 'Import Standardized ABBA Project (Zip)'. The session itself is not modified.

## Inputs

- `downscale_deformation_field` (int) **Deformation field downscaling factor**, default `4`
  The deformation field (atlas coordinates of each pixel) is computed every N pixels of the exported slices.
- `experiment_information` (String) **Experiment information**
  Free text describing the experiment (animal, staining, sectioning...), stored in the metadata of the zip.
- `identifier` (String) **Export identifier**
  Short name of the export, used in the zip file name: abba_export_<identifier>.zip.
- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session to export.
- `output_folder` (File) **Output folder**
  Folder where the zip is written. A zip with the same name must not exist.
- `pixel_size_um` (double) **Pixel size of the exported slices (micrometers)**, default `20.0`
  The original slice images are downscaled to this pixel size to keep the zip small.
- `slice_channels_csv` (String) **Slice channels**, default `*`
  0-based indices of the slice channels to export, comma separated (e.g. '0,2'), or '*' for all channels.

## Outputs

- `success` (Boolean): True if the zip was created.


# ABBA - Export Regions To File

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Regions To File`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportRegionsToRoisetFileCommand`

Saves the atlas regions of each selected slice as an ImageJ ROI set zip file, named after the slice, with ROIs in the pixel coordinates of the original (unregistered, full resolution) slice image.

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `naming_choice` (String) **ROI naming**
  Atlas ontology property used to name each region ROI, for instance its acronym, name or id. The available choices depend on the atlas.
- `dir_output` (File) **Output folder**
  Folder where one '<slice name>.zip' ROI set is written per selected slice.
- `erase_previous_file` (boolean) **Overwrite existing files**
  If checked, existing ROI set files with the same name are replaced; otherwise these slices are skipped with a warning.


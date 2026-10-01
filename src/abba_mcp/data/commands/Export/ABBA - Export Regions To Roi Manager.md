# ABBA - Export Regions To Roi Manager

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Export > ABBA - Export Regions To Roi Manager`  
Class: `ch.epfl.biop.atlas.aligner.command.ExportRegionsToRoiManagerCommand`

Adds the atlas regions of each selected slice to the ImageJ ROI Manager, as ROIs in the pixel coordinates of the original (unregistered, full resolution) slice image.

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `naming_choice` (String) **ROI naming**
  Atlas ontology property used to name each region ROI, for instance its acronym, name or id. The available choices depend on the atlas.


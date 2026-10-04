# Open Atlas

Menu: `Plugins > BIOP > Atlas > Open Atlas`  
Class: `ch.epfl.biop.atlas.scijava.AtlasChooserCommand`

Opens a brain atlas, the first step of an ABBA session: its output is the input 'ba' of 'ABBA - ABBA Start' and 'ABBA - Align Big Brains and Atlases (no GUI)'. The atlases offered are computed when the command starts: the built-in ones and the BrainGlobe atlases already downloaded, then the BrainGlobe atlases not downloaded yet, once the catalogue was fetched ('List BrainGlobe Atlases' lists all of them, and which are downloaded).

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `choice` (String) **Choose an atlas**
  Atlas name. Names ending in '_java' are built into ABBA (allen_mouse_10um_java: Allen mouse CCFv3.1; whs_sd_rat_39um_java: Waxholm rat v4.2). Names with '@' and a version (allen_mouse_25um@3.0) are BrainGlobe atlases, downloaded once, which can take minutes and a few GB: any published one opens by its name and version, listed by 'List BrainGlobe Atlases'. 'Get BrainGlobe Atlases...' opens a window to choose one.
- `additionalAtlases` (String) **Additional atlases (comma-separated, optional)**, optional
  Comma-separated atlas names whose structural channels will be merged into the principal atlas via CompositeAtlas. Leave empty for a plain atlas.

## Outputs

- `atlas` (Atlas)


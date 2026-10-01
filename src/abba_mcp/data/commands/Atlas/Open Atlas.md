# Open Atlas

Menu: `Plugins > BIOP > Atlas > Open Atlas`  
Class: `ch.epfl.biop.atlas.scijava.AtlasChooserCommand`

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `choice` (String) **Choose an atlas**
- `additionalAtlases` (String) **Additional atlases (comma-separated, optional)**, optional
  Comma-separated atlas names whose structural channels will be merged into the principal atlas via CompositeAtlas. Leave empty for a plain atlas.

## Outputs

- `atlas` (Atlas)


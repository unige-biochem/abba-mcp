# List BrainGlobe Atlases

Menu: `Plugins > BIOP > Atlas > List BrainGlobe Atlases`  
Class: `ch.epfl.biop.atlas.scijava.BrainGlobeAtlasListCommand`

Lists every atlas published by BrainGlobe (the latest version of each), and the ones already downloaded on this computer. Any of them opens with 'Open Atlas', with its name and version as the choice (e.g. allen_mouse_25um@3.0): one not downloaded yet is downloaded first (minutes, up to a few GB). The first listing of a Fiji session needs BrainGlobe's Python environment, which takes minutes to build the first time on a computer. Afterwards, 'Open Atlas' offers the whole list too.

## Inputs

- `filter` (String) **Filter**, optional
  Only the atlases whose name contains all these words, separated by spaces (e.g. 'mouse', 'rat 25um'). Empty for all.

## Outputs

- `atlases` (String): A summary line, then one atlas per line: its name and version, followed by '(downloaded)' for the ones on this computer.


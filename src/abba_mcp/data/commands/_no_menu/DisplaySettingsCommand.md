# DisplaySettingsCommand

Class: `ch.epfl.biop.atlas.aligner.command.DisplaySettingsCommand`

Sets the display settings (range and color) of a channel of the slices selected in the slices table.

**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them.

## Inputs

- `min` (double) **Display min**
  Pixel value displayed as black.
- `max` (double) **Display max**
  Pixel value displayed at full brightness; higher values are saturated.
- `color` (ColorRGB) **Color**
  Display color of the channel.
- `postrun` (Consumer), optional

## Outputs

- `ds` (Displaysettings)


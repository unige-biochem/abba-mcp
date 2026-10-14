# ABBA - Set Slice Background

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Set Slice Background`  
Class: `ch.epfl.biop.atlas.aligner.command.SetSlicesBackgroundCommand`

For brightfield images with a white background: the area outside of the selected slices images is filled with this value instead of black, which avoids dark edges during registrations and exports. Works for 8-bit, 16-bit and RGB images.

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `white_background_value` (int) **Background value**, default `255`
  Pixel value used outside of the images: 255 for 8-bit or RGB images, 65535 for 16-bit images.


# ABBA - Set Region Of Interest

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > Edit > ABBA - Set Region Of Interest`  
Class: `ch.epfl.biop.atlas.aligner.command.SetRegionOfInterestCommand`

Sets the rectangular region of interest (ROI) of the session: registrations only consider this region, and exports to images are cropped to it. It applies to all slices. For hemi-sections, restrict it to the hemisphere, and restore the full size afterwards. 'ABBA - Get State' gives the current one (roi_mm).

## Inputs

- `mp` (MultiSlicePositioner) **ABBA session**
  The ABBA session the command acts on.
- `region_mm` (String) **Region (mm)**, optional
  'x,y,width,height' in mm, x and y being the top left corner, in the coordinates of the rulers of 'ABBA - Snapshot' (the full atlas section is centred on 0). Empty for the full atlas section.

## Outputs

- `roi_mm` (String): The region now in use: x,y,width,height in mm.


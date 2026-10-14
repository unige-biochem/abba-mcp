# Images and import

## Before import (on the user's side)

- **Calibration.** Images must carry a physical pixel size (µm or mm). An uncalibrated image is assumed to be
  1 µm per pixel and looks gigantic next to the atlas. Fix the pixel size in QuPath *before* importing.
- **One QuPath project per animal**, and do not add or remove images in the project after the ABBA import.
- **Pyramidal files.** Without a resolution pyramid, downsampling for registration aliases and everything is
  slow (fine below about 2000×2000 pixels). Good formats: `.vsi`, `.czi`, pyramidal `.ome.tif`. Leica `.lif`
  pyramids are not read by Bio-Formats; OpenSlide-only formats are not supported. Convert with Kheops or to
  OME-TIFF if needed.
- 16-bit RGB images (some CZI) need their RGB channels split: only `ABBA - Import With Bio-Formats` and
  `ABBA - Import QuickNII Project` offer `split_rgb_channels`.

## Import

- `ABBA - Import QuPath Project`: `qupath_project`, `first_slice_position_mm`, `slice_spacing_mm` (not 0; a
  negative value reverses the order). Positions use the displayed convention (0 = front of the atlas).
  Advanced options of the QuPath dataset (plane origin, RGB split) are not inputs of this command.
- `ABBA - Import With Bio-Formats`: files directly, when there is no QuPath project. The results can still go
  to QuPath: `ABBA - Export Slices To New QuPath Project` creates the project afterwards.
- Demo data: `ABBA - Open Demo Slices From ZENODO` (1 to 7 slides, cached locally) or
  `ABBA - Open Demo Slices From OMERO` (25 or 97 sections, streamed from the German BioImaging OMERO server
  through a shared read-only account: no credentials needed. A credentials dialog means the connection
  failed: tell the user, do not ask for a password). `project_directory` keeps the demo's QuPath project, to
  export registrations into: the command creates it if needed. Importing the demo again in the same Fiji reuses
  the first import's images, and their project: stop Fiji first (`abba_fiji_stop`, after saving).
  A state saved from the demo, loaded in another Fiji, asks for OMERO credentials: connect first with
  `Omero - Connect` (host `omero-tim.gerbi-gmb.de`, port 4064, the demo's public read-only account:
  username and password `read-tim`), then load the state.
- Slide scanner files (e.g. `.vsi`) also contain a label, an overview and a macro image: they become extra,
  dark RGB "slices". Point them out (`ABBA - Get State` gives names), ask, then `ABBA - Delete Slices`.

## Display ranges

- They matter for **DeepSlice only**: slices are sent to it as 8-bit RGB with their current colour and
  min/max. Saturation ruins the result; ABBA itself warns that almost half of the images users send to
  DeepSlice are over-saturated. Elastix does not use display settings.
- `ABBA - Auto Display Range` sets them from percentiles of the pixel values (0.1 to 99.9 by default), one range
  per channel for all the selected slices. `ABBA - Set Slices Min Max Display Range` sets given values. Then render
  one slice (`ABBA - Snapshot` without borders and labels) and look: tissue clearly visible, not clipped.
- Unsaturating raises the maximum (a lower maximum clips more). A single bright artefact makes the 100th
  percentile useless: try a high percentile between 99.9 and 99.99, and compare snapshots before and after.
- Brightfield: also `ABBA - Set Slice Background`.

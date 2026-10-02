# State files, coordinates and exports

## The state file (`.abba`)

- `ABBA - Save State` writes a `.abba` file: a zip of `_bdvdataset_{i}.xml` (how to open the images, possibly
  with absolute paths), `sources.json` (source names, display settings) and `state.json` (per slice, the list
  of actions: creation, moves, registrations; plus the atlas slicing angles). It refuses to overwrite a file.
- A state **does not contain images**. Moving the image files, changing drive letters or editing the QuPath
  project can break re-opening. It must be reopened with the same atlas (`ABBA - Load State`, into an empty
  session).
- Keep successive state files. The long-lived deliverable is the regions exported to QuPath; the `.abba`
  format is for continuing work.
- Positions in `state.json` (`location`) are the stored convention (`slicing_axis_position`), not the
  displayed `z_mm`. `ABBA - Get State` returns the same content with both, plus names and indices.

## What a registration is

- Per slice, the stored transform maps **atlas → slice pixel** (forward). Its numerical inverse gives
  slice pixel → atlas, used to place detections in the atlas; it can fail for extreme splines.
- Atlas coordinate images (`ABBA - Export Atlas Coordinates of Original Slices to ImageJ`) are 32-bit, in mm.

## Exports, by preference

1. **Regions onto the original images** (no image is deformed, fastest):
   `ABBA - Export Registrations To QuPath Project` writes, per image entry, `ABBA-RoiSet-<atlas>.zip` and
   `ABBA-Transform-<atlas>.json`, plus the atlas ontology next to the project (do not delete it). In QuPath,
   the ABBA extension imports them (`AtlasTools.loadWarpedAtlasAnnotations`). Slices opened from files (one
   series of a 2D file, Bio-Formats) have no QuPath project: `ABBA - Export Slices To New QuPath Project` creates
   one (QuPath 0.7, empty or new folder) with the images and the same files. Also
   `ABBA - Export Regions To File` (ROI set per slice, without QuPath) and `ABBA - Export Regions To Roi Manager`.
2. **Rasterized images in atlas space**: `ABBA - Export Registered Slices to ImageJ` and
   `ABBA - Export Atlas to ImageJ`, with the same `pixel_size_um` and ROI so that they overlay. Start coarse
   (20 to 40 µm): halving the pixel size multiplies time by 4, and ImageJ caps a plane at 2 gigapixels.
3. **3D reconstruction**: `ABBA - Export Registered Slices to BDV` (experimental variants exist).
4. **Interchange**: `ABBA - Export registered slices as QuickNII dataset` (lossy: 8-bit, at most 3
   channels, JPEG by default); `ABBA - Export Standardized ABBA Project (Zip)` (all slices, to reopen elsewhere).

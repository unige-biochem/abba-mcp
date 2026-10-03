# ABBA with the module tools: workflow and traps

ABBA registers 2D histological sections to a 3D reference atlas. Each section ("slice") gets a position
along the atlas slicing axis, then a stack of in-plane registrations (affine, spline...) that map the atlas
onto it. The result is used to assign brain regions to cells, usually in QuPath.

See also: `images-and-import.md` (calibration, formats, display), `storage-and-exports.md` (state files,
coordinates, exports), `window.md` (the ABBA window, working with the user in it). Commands: `../commands/INDEX.md`.

## How the tools work

- Every ABBA action is a SciJava command, run by its title with `fiji_module_run(id, inputs)`, where `inputs` is a
  JSON object. `fiji_module_describe` gives a command's inputs, defaults and choices, and the version providing it.
- Commands never open a dialog for you: inputs not given keep their default. An object input (the ABBA session `mp`,
  the atlas `ba`) with a single live instance is filled in, otherwise pass its name: `fiji_objects` counts the live
  objects per type, and lists one type by name (e.g. `MultiSlicePositioner`).
- **Commands act on the session, never on a window.** A window (there may be several) shows the session to the user.
  Point at slices with the selection, which every window draws; look at a window with `fiji_ui_screenshot`.
- Registration commands queue work and return at once. `ABBA - Get State` and `ABBA - Snapshot` wait for the queued
  work: use them to know when it is done and how it went.

## Before starting: ask the user

- **The atlas.** `Open Atlas` lists what is available (describe it: the list is computed at runtime).
  `allen_mouse_10um_java` (Allen mouse CCFv3.1) and `whs_sd_rat_39um_java` (Waxholm rat v4.2) are built in;
  names like `allen_mouse_25um@3.0` are BrainGlobe atlases, downloaded on demand. Avoid the
  `Get BrainGlobe Atlases...` and "not downloaded yet" entries without asking: they download or open a window.
- **How the sections were cut**, which sets the axes of `ABBA - ABBA Start`:
  coronal x=`RL (Right-Left)`, y=`SI (Superior-Inferior)`, z=`AP (Anterior-Posterior)`;
  sagittal x=`AP`, y=`SI`, z=`LR`; horizontal x=`LR`, y=`AP`, z=`SI` (full choice strings in the command doc).
- **Where the images are.** A QuPath project is the recommended input: results go back into it. **One
  project per animal**: the atlas slicing angle is shared by all slices of a session.
- If known: position of the first section and spacing (otherwise import positions are placeholders), which
  channel holds what (nuclei, autofluorescence...), and whether sections are whole or hemi-brains.

## Typical order

| Step | Commands |
|---|---|
| 1. Atlas, session | `Open Atlas`, then `ABBA - ABBA Start` (window) or `ABBA - Align Big Brains and Atlases (no GUI)` |
| 2. Import | `ABBA - Import QuPath Project` (preferred), `ABBA - Import With Bio-Formats`; demo: `ABBA - Open Demo Slices From ZENODO` |
| 3. Remove non-sections | `ABBA - Get State` (names), ask, `ABBA - Delete Slices` |
| 4. Orientation | `ABBA - Rotate` (Z any angle; X/Y only ±180 = flip), `ABBA - Mirror Slices` for hemi-sections |
| 5. Display ranges (DeepSlice only) | `ABBA - Auto Display Range` (percentiles, no saturation), or `ABBA - Set Slices Min Max Display Range` |
| 6. Position + slicing angle | `ABBA - DeepSlice Registration`, on all slices of the animal at once |
| 7. Affine | `ABBA - Elastix Registration (Affine)` |
| 8. Spline (once or twice) | `ABBA - Elastix Registration (Spline)` |
| 9. Check | `ABBA - Snapshot` on all slices, then on doubtful ones without labels, zoomed with `region_mm` |
| 10. Save, export | `ABBA - Save State`, `ABBA - Export Registrations To QuPath Project` (or `ABBA - Export Slices To New QuPath Project` for slices opened from files), `fiji_module_script` |

A complete, tested run of steps 1-9 on demo data: `../examples/abba_demo_pipeline.groovy`.

## Choosing inputs

- **Channels are paired in order** for Elastix: `atlas_channels_csv` `0,1` with `slice_channels_csv` `0,1`
  pairs atlas channel 0 (Nissl for Allen) with slice channel 0 (e.g. DAPI) and atlas channel 1 (Ara,
  autofluorescence-like) with slice channel 1. The atlas channels in index order are `atlas_channels` in
  `ABBA - Get State`. Lists must have the same length; `*` is not accepted; a channel
  may be repeated; each pair weighs equally. Selected slice channels must share a pixel type.
- **Elastix affine** `pixel_size_um` 40 is a good start. **Spline** `nb_control_points_x` 5 to 20 (more is
  more flexible and risks overfitting where tissue and atlas differ; 12 to 15 is common), `pixel_size_um` 20.
- **DeepSlice** `model` must match the species. `post_processing`: for serial sections of one animal use
  `Keep order + ensure regular spacing` (or `Keep order + set spacing` when the cutting interval is known).
  Plain `Keep order` keeps DeepSlice's raw spacing, which can put two consecutive sections a micrometre apart:
  check the positions in `ABBA - Get State` after DeepSlice.
  Try `ensemble` both ways. With 2 slices or fewer, the angle is not propagated.
- Reference recipe from the documentation: affine then spline with DAPI↔Nissl and autofluorescence↔Ara,
  15 control points; about 10 minutes for 50 slices on a laptop.

## Traps

- **Selection.** Most commands act on the *selected* slices. `ABBA - Select Slices` adds to the selection,
  `ABBA - Deselect Slices` removes. Indices are 0-based along the slicing axis and **change when a slice moves**:
  re-read the state after DeepSlice or any move.
- **Labels are not observations.** A snapshot draws the atlas at the slice's current position. After an
  import that position is a placeholder (`reg=0` in the header). Turn labels and borders off to see the tissue.
- **Positions come in two conventions**: `z_mm` (displayed, atlas convention, 0 = front of the atlas) and
  `slicing_axis_position` (stored in state files). `ABBA - Get State` gives `z_mm`, and both with `full`.
- **Registrations stack per slice** and apply in sequence. `ABBA - Remove Last Registration` pops one per
  selected slice (positions are not affected). `ABBA - Undo or Redo` undoes whole commands: one step reverts
  a registration of all the slices it ran on. The atlas slicing angles are not undone.
- **Broken or missing tissue** registers badly with splines: expect local failures there, and look.
- **Hemi-sections**: restrict the region with `ABBA - Define Rectangular ROI` (mm, atlas section centred on 0)
  or mirror before DeepSlice. The ROI also crops exports: restore it afterwards.
- **Brightfield** (white background): `ABBA - Set Slice Background` (about 200-255 for 8-bit) so that areas
  outside the image are not black, which would bias registration.
- **Loading a state** (`ABBA - Load State`) adds its slices to the current session: start from an empty one,
  with the same atlas.

## Positioning without DeepSlice

When DeepSlice is not suitable, or got a slice wrong, position by hand, then check with snapshots:
`ABBA - Move Slices` (indices and positions in mm, displayed convention), `ABBA - Set Key Slices` on the 2 or 3
slices you trust, then `ABBA - Distribute Slices` on the selection (first, last and key slices stay, the others
are spaced evenly), and `ABBA - Set Atlas Slicing Angles` for the cutting angle (not undoable: note the
current angles first). Indices change after every move: re-read the state.

Commands that need a window and a person: `ABBA - Manual Affine Registration`, `ABBA - BigWarp Registration`,
`ABBA - Edit Last Registration`, `ABBA - Adjust Slicing`. Do not use the obsolete
`ABBA - DeepSlice Registration (Web)` / `(Local)`.

## When something disagrees with what you expected

Question what the expectation was built on before blaming the tool: a placeholder position, a saturated
channel, a wrong channel pairing, an uncalibrated image. Then look again, on one slice, without labels.

## Citing

`ABBA - Get Prompt for Methods Writing` (selected slices) produces a methods paragraph with the citations
for ABBA (Cell Reports 2025, doi 10.1016/j.celrep.2025.115876), the atlas, DeepSlice, Elastix and BrainGlobe
as used.

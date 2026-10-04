# The ABBA window: coaching, looking, scripting

The window opened by `ABBA - ABBA Start` is a **view** of the session (Java class
`ch.epfl.biop.atlas.aligner.gui.bdv.BdvMultislicePositionerView`, a BigDataViewer window). Commands act on the
session, never on a view: what a command changes shows in every view. A session started with
`ABBA - Align Big Brains and Atlases (no GUI)` has no view at all. See also: `abba.md`.

## What the window shows

Title: `Aligning Big Brains and Atlases - <atlas name>`, then ` (view 2)`, ` (view 3)`... for further views of the
same session, with `* (modified)` appended while there are unsaved changes. The title without that marker is the
view's name in `fiji_objects`. `abba_window_picture` takes the title or its start (`fiji_ui_windows_read` lists them). The window opens
maximized: the viewer on the left, the cards on the right (about 600 px).

Drawn on the viewer: top left, the current slice's name (`[Key]` for a key slice), `Z: <mm> mm (Thickness: <um> um)`
and the list of its actions; top centre, `N tasks running` while work is queued; bottom left,
`Modified since last save!` or `No modification`; at the mouse pointer, the atlas region and its parents
(`Region<Parent<...`) and the atlas coordinates `[x;y;z]` with `(L)` or `(R)`. Info messages pass briefly.

Each slice has a **round handle**: green if selected, yellow if not, larger for key slices. The current slice has
a light grey circle and `◄ ►`. Under a handle, one marker per action: a registration is an `R` in a circle
(automatic) or a square (manual), light red while waiting, yellow while running, green when done; small and grey
when hidden by `View Previous`.

| Mode | Shows |
|---|---|
| Positioning (at start) | Atlas sections side by side along the slicing axis, one every "Displayed slicing [atlas steps]"; the slices below them (overlap mode: on the atlas, below, or below in stairs, the default). Under the atlas row, a small square per slice, linked to its handle by a dashed line: it is what one drags. Selected slices are joined by a magenta line. |
| Review | The current slice only, over the atlas cut at its position. The handles form a row near the top. Slices cannot be dragged. |

Switch: key `R`, buttons `Review` / `Positioning` in the Display & Navigation card, `View > Display Mode`, or the
right-click menu.

## Cards (right panel)

| Card | For |
|---|---|
| Atlas Information | Atlas name, size and resolution, modalities, DOI, `WebPage` button. |
| Atlas Display | Per atlas channel, a checkbox `<name> (Ch. i)` (i = the index used in registration commands) and a brightness slider; "Displayed slicing [atlas steps]" (1-50), the spacing of the atlas sections in positioning mode. |
| Slices Display | Current slice name and info; a table, one row per slice: `#` (index as in the commands, name, `(Key)`), `Vis.`, then per channel `Ch_i` (visibility) and an unnamed column (colour and range). Selecting rows selects slices. Clicking a column header applies to the selected rows. Double-click a name: it becomes the current slice. `Filter by name` field. |
| Display & Navigation | `Review` / `Positioning`; `Display One Slice Only (fast)` / `Display All Slices` (positioning only); `Change Overlap Mode` and overlap size sliders; `Previous [Left]`, `Center Current [C]`, `Next [Right]`; `View Previous [P]` / `View Next [N]`. |
| Edit Selected Slices | Rotate 90° clockwise or counter-clockwise, flip around X or Y (as `ABBA - Rotate`), `Distribute Spacing` (as `ABBA - Distribute Slices`). |
| Atlas Slicing | `Lock rotations`, `X rotation (degrees)` and `Y rotation (degrees)` sliders (±45): the interactive form of `ABBA - Adjust Slicing`. You: `ABBA - Set Atlas Slicing Angles`. |
| Define Region Of Interest | Collapsed at start. X, Y, Width, Height (mm), `Define Interactively` (draw it in the viewer), `Full Size`: `ABBA - Define Rectangular ROI`. You: `ABBA - Set Region Of Interest`. |

`View > Cards > Add Resources Monitor` adds a CPU and memory card.

## Mouse and keyboard

| Action | Key or gesture | Mode |
|---|---|---|
| Select slices (replace) | Left-drag a rectangle around the round handles, starting on empty space | both |
| Add to / remove from selection | Shift + left-drag / Ctrl + left-drag (press the key first) | both |
| Select all / deselect all | Ctrl+A / Ctrl+Shift+A (Cmd on Mac); or rows of the Slices Display table | both |
| Move slices along the axis | Left-drag the small square of a selected slice: all selected slices move, except that a selected key slice stays, with the selected slices beyond it, and those between are stretched | positioning |
| Deselect one slice | Right-click its small square | positioning |
| Context menu | Right-click: key slices, remove selected slices, edit or remove last registration, undo/redo, mode, overlap | both |
| Pan / zoom | Right-drag / wheel, Up and Down arrows (Shift: faster) | both |
| Current slice: next, previous, centre | Right, Left (wraps around), C | both |
| Switch mode | R | both |
| Show earlier registrations / back | P / N (all slices of this view) | both |
| Overlap mode | O | positioning |
| Distribute selected slices | D | positioning |
| Undo / redo | Ctrl+Z / Ctrl+Y or Ctrl+Shift+Z | both |
| Import | Drop a `.qpproj` (imports) or an `.abba` (loads, empty session only) on the viewer | both |

There is no on-screen key help: `K` only writes the bindings to the debug log. Menu labels show some keys.

## Menus

Menu items run the same commands as `fiji_module_run`, with their dialog (same inputs as `fiji_module_describe`).

| Menu item | Command |
|---|---|
| `Import > Import QuPath Project` / `Import With Bio-Formats` | `ABBA - Import QuPath Project` / `ABBA - Import With Bio-Formats` |
| `Slices > Select Slices` / `Deselect Slices` | `ABBA - Select Slices` / `ABBA - Deselect Slices` |
| `Slices > Set Slices Display Range` | `ABBA - Set Slices Min Max Display Range` |
| `Slices > Set White Background` | `ABBA - Set Slice Background` |
| `Register > DeepSlice > DeepSlice Registration` | `ABBA - DeepSlice Registration` (model preset from the atlas) |
| `Register > Affine > Elastix Registration (Affine)` / `Manual Affine Registration` / `Rotate` | same titles, prefixed `ABBA - ` |
| `Register > Spline > Elastix Registration (Spline)` / `BigWarp Registration` | same titles, prefixed `ABBA - ` |
| `Register > Edit Last Registration` / `Remove Last Registration` | same titles, prefixed `ABBA - ` |
| `Register > Copy Registrations From Model And Apply To Selected Slices` | `ABBA - Copy and Apply Registration` |
| `Export > QuPath > Export Registrations To QuPath Project` | `ABBA - Export Registrations To QuPath Project` |
| `Cite > Generate Methods Prompt` | `ABBA - Get Prompt for Methods Writing` |

Not commands, but equivalent: `Slices > Remove Slices` (`ABBA - Delete Slices`), `Slices > Distribute Slices [D]`
(`ABBA - Distribute Slices`, positioning mode only), `Edit > Undo` / `Redo` (`ABBA - Undo or Redo`),
`File > Save State (+View)` (`ABBA - Save State` plus the view file, below). Old tutorials: there is no
`Register > Affine > Interactive Transform` any more, and DeepSlice Web/Local are under `Edit > Obsolete`.

## Working with the user

- **Point with the selection, not the current slice.** The selection belongs to the session and shows in every
  view (green handles, selected table rows); the current slice belongs to one view and commands cannot see it.
  Ask the user to select the slices they mean, then read `selected` in `ABBA - Get State`; or select with
  `ABBA - Select Slices` and tell them to look for the green handles. The table's `#` is the command index.
- **Look** with `abba_window_picture` (the title or its start, default the first ABBA window;
  `fiji_ui_windows_read` lists the titles). It draws the window into a picture, so it is right when the window is
  covered or the screen is locked, and never shows another application; it does not show the mouse pointer, nor
  dialogs (separate windows: picture them by title). It is left out of `fiji_module_script`. To judge a
  registration, prefer `ABBA - Snapshot`, which does not depend on the window and its zoom.
- **Error and warning messages** reach you first, in the run's `messages` (or its error), then the user in a
  dialog of the window; the command does not wait for the dialog. `fiji_ui_dialogs_read` lists the dialogs still
  open; answer one (`fiji_ui_dialog_respond`, a button) or close it (`fiji_ui_dialog_close`) only if the user asks.
- **Interactive commands** return at once: the window opens when the slices' queued work reaches it, one at a
  time (a lock serialises manual editions). `ABBA - Get State` waits until the user has finished; run it with
  a short `wait_seconds`, then follow the job id with `fiji_module_status`. Or watch `fiji_ui_windows_read`.

| Command | What opens for the user | How it ends |
|---|---|---|
| `ABBA - Manual Affine Registration` | One window `Manual Affine Registration` for all selected slices, card `Affine transformation`: drag the handles (white translate, red/green axes, yellow rotate-scale, Shift constrains), `Previous`/`Next` or arrows between slices, `Apply each change to all n slices` (on by default), `Reset` | `Apply transformation`; `Cancel` or closing the window adds nothing |
| `ABBA - BigWarp Registration` | BigWarp, one slice after the other, and a dialog `BigWarp Registration` with the key help | `OK` in that dialog; closing it also accepts. No cancel: undo afterwards |
| `ABBA - Edit Last Registration` | Per selected slice whose last registration is editable: Elastix spline → BigWarp with its landmarks and a dialog `Edit Spline Registration`; BigWarp → BigWarp again, dialog `BigWarp Registration`; affine → the affine editor, titled `Edit <registration name>` | `OK`; `Apply transformation` / `Cancel` |
| `ABBA - Adjust Slicing` | Nothing through `fiji_module_run`: its `reslicedAtlas` input is not a live object, so it most likely cannot run there. Use `ABBA - Set Atlas Slicing Angles`; the user uses the Atlas Slicing card | - |

- **Closing the window** asks `Are you sure you want to exit ABBA?`, then `Close session and clear memory ?`.
  No to the second keeps the session alive without a view; Yes closes it. `ABBA - Close session` while the
  window is open leaves the window on a dead session (an error message says so).

## Several views

No command opens a second view of a session: `ABBA - ABBA Start` always creates a new session. A script can
(untested): `new BdvMultislicePositionerView(mp, new DefaultBdvSupplier(new SerializableBdvOptions()).get())`
(`sc.fiji.bdvpg.viewer.bdv.supplier`); it shows the existing slices and registers itself, named and titled
`... (view 2)`. Closing one with "clear memory" closes the session for all.

| Per view | Per session |
|---|---|
| Mode, current slice, viewer zoom and position, overlap mode and sizes, one/all slices display, slice and channel visibility (table), atlas channel visibility, `View Previous` step, mouse overlays (`Edit > Configuration > Mouse Options`) | Slices, positions, selection, key slices, registrations, ROI, atlas slicing angles, slice display ranges and colours (`ABBA - Set Slices Min Max Display Range`, saved in the state), atlas brightness, and the "Displayed slicing" step (shared by all views although it is a display setting) |

View settings are not in the state file. `File > Save State (+View)` also writes `<name>_bdv_view.json` next to
the `.abba` (mode, one/all display, overlap mode, viewer transform, displayed step, current slice, per-slice
visibility and display); `File > Load State (+View)` reads it back, into an empty session only.
`ABBA - Save State` and `ABBA - Load State` ignore it.

## Scripting a view (rarely)

Only for what no command does (show the user a slice, a mode, a channel). Run the script with
`fiji_module_run` (id = file path). One view is bound automatically; with several, pass its name (`fiji_objects`).
The window's buttons call these methods on the Swing thread: do the same.

```groovy
#@ ch.epfl.biop.atlas.aligner.gui.bdv.BdvMultislicePositionerView view
#@ Integer slice_index
#@output String shown

import ch.epfl.biop.atlas.aligner.gui.bdv.BdvMultislicePositionerView
import javax.swing.SwingUtilities

def slice = view.msp.getSlices().get(slice_index)
SwingUtilities.invokeAndWait({
    view.setDisplayMode(BdvMultislicePositionerView.REVIEW_MODE_INT)
    view.navigateSlice(slice)
} as Runnable)
shown = slice.getName()
```

| Public member | Does |
|---|---|
| `void setDisplayMode(int mode)`, `int getDisplayMode()`, `void nextMode()` | Mode: `POSITIONING_MODE_INT` (0), `REVIEW_MODE_INT` (1) |
| `void navigateSlice(SliceSources slice)` | Makes it the current slice and centres on it |
| `void navigateNextSlice()`, `void navigatePreviousSlice()`, `void navigateCurrentSlice()` | Right, Left, C |
| `Object getCurrentSlice()`, `int getCurrentSliceIndex()` | The current slice (a `SliceSources`, or a plain `Object` if there is none) and its index |
| `void setSliceDisplayMode(int sliceDisplayMode)` | Positioning: `ALL_SLICES_DISPLAY_MODE` (0), `CURRENT_SLICE_DISPLAY_MODE` (1), `NO_SLICE_DISPLAY_MODE` (2) |
| `void setSliceChannelVisibility(SliceSources slice, int iChannel, boolean visible)`, `void setSliceVisibility(SliceSources slice, boolean visible)` | Visibility in this view |
| `void setSelectedSlicesVisibility(int iChannel, boolean visible)` | Channel visibility of the selected slices, this view |
| `void setAtlasChannelVisibility(int iChannel, boolean visible)`, `boolean getAtlasChannelVisibility(int iChannel)` | Atlas channel; the Atlas Display card does not reflect it |
| `void centerOnAtlas()`, `void centerOnAtlas(double atlasZ)` | Fits an atlas section (middle, or at `atlasZ`, displayed convention) to the window |
| `void viewPreviousRegistration()`, `void viewNextRegistration()`, `void toggleOverlap()` | P, N, O |
| `void saveState(File stateFileIn)` | State plus view file; refuses an existing file (with a dialog) |
| `void setBlockingMessages(boolean blocking)` | `false`: errors and warnings go to the viewer overlay instead of dialogs (neither blocks the command) |
| `MultiSlicePositioner msp` (field), `BdvHandle getBdvh()` | The session; the BigDataViewer handle |

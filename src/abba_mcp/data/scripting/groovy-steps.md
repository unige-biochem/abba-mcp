# Writing ABBA steps as Groovy scripts

A Groovy script with `#@` parameters is a module: it runs in Fiji's script editor (with a dialog), through
`fiji_module_run` (its file path is its id, inputs as JSON) or `fiji_module_run_script` (its code as text, no file
needed), and one-shot in a pipeline. Write the user's pipeline this way, next to their data. Before writing code,
check that no command does the step.

## Skeleton

```groovy
// Inputs: the values that vary. Outputs: what the caller gets back.
#@ File (style = "directory") output_dir
#@ String (value = "allen_mouse_10um_java") atlas_name
#@ CommandService command
#@ org.scijava.module.ModuleService modules
#@output String summary

import ch.epfl.biop.atlas.aligner.MultiSlicePositioner

def run = { String cls, Map inputs -> modules.run(command.getCommand(cls), true, inputs).get() }

def atlas = run('ch.epfl.biop.atlas.scijava.AtlasChooserCommand', [choice: atlas_name, additionalAtlases: '']).getOutput('atlas')
MultiSlicePositioner mp = run('ch.epfl.biop.atlas.aligner.command.ABBAStartCommand', [ba: atlas,
    x_axis: 'RL (Right-Left)', y_axis: 'SI (Superior-Inferior)', z_axis: 'AP (Anterior-Posterior)']).getOutput('mp')
// ... import, register ...
mp.waitForTasks()                             // registrations are queued: wait before reading or saving
summary = mp.getSlices().size() + ' slices'
```

## Rules

- A line starting with `#@` declares a parameter even inside a string: a script that writes another script
  builds such lines as `'#' + '@ ...'`.
- No comment at the end of a `#@` line: SciJava then does not recognise the parameter, and Groovy fails
  on the `#`. Put comments on their own lines.
- Call commands with `modules.run(command.getCommand('<class>'), true, [inputs])`. **Not** `command.run(...)`:
  it returns `null` for dynamic commands (such as `Open Atlas`, the exports, `ABBA - Adjust Slicing`), a known
  SciJava design flaw.
- Pass **every** input of a command. In a Fiji with a window, a missing input opens a dialog and blocks.
  The class name and the inputs of each command are in `../commands/` (or `fiji_module_describe`).
- Pass objects, not names: `mp: mp`, `ba: atlas`, taken from the outputs of earlier steps.
- To act on the session already open (`fiji_module_run_script`), declare it with its full class name, as every
  object input (`#@` lines ignore imports): `#@ ch.epfl.biop.atlas.aligner.MultiSlicePositioner mp`. A single
  session is bound by itself; with several, pass its name (`{"mp": "ABBA Instance #0"}`, see `fiji_objects`).
- Commands that register slices return before the work is done: `mp.waitForTasks()` (or `ABBA - Wait`, or
  `ABBA - Snapshot`, which waits) before saving or exporting. Queued work that failed does not stop the script:
  `mp.getFailures(0)` lists the failures of the session (`toString()`: one line each).
- To save a picture: `ABBA - Snapshot` outputs an `ImagePlus`; `ImageIO.write(img.getBufferedImage(), 'png', file)`.

## Reading the session in a script

Read values from the session, never copy them from an earlier output into the script.

| Member | Gives |
|---|---|
| `mp.getSlices()`, `mp.getSelectedSlices()` | the slices (`SliceSources`), in order along the slicing axis: the list index is the command index |
| `slice.getName()`, `slice.nChannels` | name, number of channels |
| `slice.getSlicingAxisPosition()`, then `mp.toAtlasZ(position)` | position, stored convention, then displayed `z_mm` |
| `slice.getThicknessInMm()` | thickness |
| `slice.isSelected()`, `slice.isKeySlice()` | selection, key slice |
| `slice.getNumberOfRegistrations()`, `slice.getRegistrationNames()` | registrations, in order |
| `mp.getReslicedAtlas()`, `mp.getAtlas()` | the atlas as sliced (angles, position), the atlas |
| `mp.waitForTasks()` | waits for the queued actions |

## From a session to a script

`fiji_module_script` turns the successful `fiji_module_run` calls of the session into such a script, every
input explicit and objects wired from step to step. Then: drop the inspection steps, turn the values that
vary into `#@` parameters, declare `#@output`s, and run it once more to check. `../examples/` shows the result.

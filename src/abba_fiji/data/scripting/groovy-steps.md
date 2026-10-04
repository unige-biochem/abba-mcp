# Writing ABBA steps as Groovy scripts

A Groovy script with `#@` parameters is a module: it runs in Fiji's script editor (with a dialog), through
`fiji_module_run` (its file path is its id, inputs as JSON), and one-shot in a pipeline. Write the user's
pipeline this way, next to their data.

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

- No comment at the end of a `#@` line: SciJava then does not recognise the parameter, and Groovy fails
  on the `#`. Put comments on their own lines.
- Call commands with `modules.run(command.getCommand('<class>'), true, [inputs])`. **Not** `command.run(...)`:
  it returns `null` for dynamic commands (such as `Open Atlas`, the exports, `ABBA - Adjust Slicing`), a known
  SciJava design flaw.
- Pass **every** input of a command. In a Fiji with a window, a missing input opens a dialog and blocks.
  The class name and the inputs of each command are in `../commands/` (or `fiji_module_describe`).
- Pass objects, not names: `mp: mp`, `ba: atlas`, taken from the outputs of earlier steps.
- Commands that register slices return before the work is done: `mp.waitForTasks()`, or run
  `ABBA - Get State` / `ABBA - Snapshot`, which wait, before saving or exporting.
- To save a picture: `ABBA - Snapshot` outputs an `ImagePlus`; `ImageIO.write(img.getBufferedImage(), 'png', file)`.

## From a session to a script

`fiji_module_script` turns the successful `fiji_module_run` calls of the session into such a script, every
input explicit and objects wired from step to step. Then: drop the inspection steps, turn the values that
vary into `#@` parameters, declare `#@output`s, and run it once more to check. `../examples/` shows the result.

# ABBA - Run Benchmark

Menu: `Plugins > BIOP > Atlas > Multi Image To Atlas > ABBA - Run Benchmark`  
Class: `ch.epfl.biop.atlas.aligner.command.ABBABenchMarkCommand`

Runs a complete ABBA workflow on a demo dataset (mouse atlas, import, two DeepSlice runs, Elastix affine and spline registrations, QuPath export for the remote datasets) and reports the time and memory used by each step.

## Inputs

- `comment` (String) **Comment**
  Free text copied in the report, for instance to describe the machine.
- `demo_dataset` (String) **Demo dataset**, one of: `25 sections (remote)`, `97 sections (remote)`, `1 slide local (cached, local)`, `97 sections (cached, local)`
  Remote datasets are streamed from a public OMERO server (needs the OMERO dependencies). Local datasets are downloaded once from Zenodo and cached (about 1 GB per slide).
- `use_gui` (boolean) **Use graphical user interface**, default `false`
  If checked, the benchmark runs in an ABBA window; otherwise it runs without display.
- `wait_between_each_step` (boolean) **Time each registration step**, default `false`
  If checked, each registration step waits for all sections to be done before the next one starts, so that each step is timed separately. Slower.

## Outputs

- `report` (String): Markdown report: configuration, time and memory per step. Also written to the ImageJ log.


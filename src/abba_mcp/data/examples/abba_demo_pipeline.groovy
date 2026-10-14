#@ String (label = "Atlas", value = "allen_mouse_10um_java") atlas_name
#@ Integer (label = "Demo slides to import (1 to 7)", value = 1) number_of_slides
#@ File (label = "Output folder", style = "directory") output_dir
#@ CommandService command
#@ org.scijava.module.ModuleService modules
#@output File state_file
#@output File snapshot_file
#@output String summary

// A complete ABBA registration of the demo dataset, without any dialog: it runs as is in Fiji's script
// editor, through fiji_module_run (headless or not), or one-shot from a pipeline.
// Born as fiji_module_script's recording of an agent session, then edited by hand:
// values that vary became #@ parameters, inspection steps were dropped, outputs were declared.
// Coronal sections: x = RL, y = SI, z = AP. Commands are run with modules.run(command.getCommand(...)):
// command.run returns null for dynamic commands such as Open Atlas (a SciJava design flaw).

import ch.epfl.biop.atlas.aligner.MultiSlicePositioner
import javax.imageio.ImageIO

def atlas = modules.run(command.getCommand(ch.epfl.biop.atlas.scijava.AtlasChooserCommand), true, [
    choice: atlas_name, additionalAtlases: '']).get().getOutput('atlas')

MultiSlicePositioner mp = modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.ABBAStartCommand), true, [
    ba: atlas, x_axis: 'RL (Right-Left)', y_axis: 'SI (Superior-Inferior)', z_axis: 'AP (Anterior-Posterior)']).get().getOutput('mp')

modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.ImportDemoSlicesZENODOCommand), true, [
    mp: mp, number_of_slides: number_of_slides]).get()
mp.waitForTasks()

// Slide files also hold a label, an overview and a macro image: only the '10x' images are sections.
def notSections = mp.getSlices().findIndexValues { !it.getName().contains('10x') }.join(',')
if (notSections) modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.DeleteSlicesCommand), true, [mp: mp, slices_csv: notSections]).get()

modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.SetSlicesSelectedCommand), true, [mp: mp, slices_csv: '*']).get()
// DeepSlice receives the slices as displayed: no saturation
modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.AutoDisplayRangeCommand), true, [
    mp: mp, slice_channels_csv: '0,1', low_percentile: 0.1d, high_percentile: 99.9d, same_range_for_all_slices: true]).get()

modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.RegisterSlicesDeepSliceApposeCommand), true, [
    mp: mp, model: 'mouse', slice_channels_csv: '0,1', allow_slicing_angle_change: true, pixel_size_um: 30.0d,
    ensemble: false, post_processing: 'Keep order + ensure regular spacing', slice_spacing_um: -1.0d]).get()
modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.RegisterSlicesElastixAffineCommand), true, [
    mp: mp, atlas_channels_csv: '0,1', slice_channels_csv: '0,1', pixel_size_um: 40.0d,
    show_imageplus_registration_result: false]).get()
modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.RegisterSlicesElastixSplineCommand), true, [
    mp: mp, atlas_channels_csv: '0,1', slice_channels_csv: '0,1', nb_control_points_x: 12, pixel_size_um: 20.0d,
    show_imageplus_registration_result: false]).get()

// Snapshot waits for the queued registrations: it is also the barrier before saving.
def snapshot = modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.SnapshotCommand), true, [
    mp: mp, slices_csv: '*', pixel_size_mm: 0.04d, atlas_channel: -1, show_region_borders: true,
    show_region_labels: false, columns: 0, slice_channels_csv: '0,1', registration_step_back: 0,
    region_mm: '']).get().getOutput('snapshot')
snapshot_file = new File(output_dir, 'abba_demo_overview.png')
ImageIO.write(snapshot.getBufferedImage(), 'png', snapshot_file)

state_file = new File(output_dir, 'abba_demo_' + System.currentTimeMillis() + '.abba')
modules.run(command.getCommand(ch.epfl.biop.atlas.aligner.command.ABBAStateSaveCommand), true, [mp: mp, state_file: state_file]).get()
summary = mp.getSlices().size() + ' slices registered (DeepSlice, Elastix affine and spline) to ' + atlas_name

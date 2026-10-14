#@script(record="false")
#@ org.scijava.object.ObjectService objects
#@ String (label = "Window title", value = "Aligning Big Brains and Atlases") window_title
#@ String (label = "Mode", choices = {"keep", "positioning", "review"}, value = "keep") mode
#@ Integer (label = "Slice index", value = -1) slice_index
#@ String (label = "Region (mm), or all", value = "") region_mm
#@ String (label = "Visible slice channels", value = "") slice_channels
#@ String (label = "Visible atlas channels", value = "") atlas_channels
#@output String view
// Sets what an ABBA window shows the user: its mode, its current slice, the channels shown, and what is framed.
// Review mode: the atlas section of the current slice, whole or a region of it in the coordinates of
// ABBA - Snapshot's region_mm. Positioning mode: the current slice and its neighbours with the atlas above them, or
// all the slices. The bundle's abba_window_view tool runs it. record="false": it only changes the view, so
// fiji_module_script leaves it out.
import bdv.viewer.SourceAndConverter
import ch.epfl.biop.atlas.aligner.MultiSlicePositioner
import ch.epfl.biop.atlas.aligner.SliceSources
import ch.epfl.biop.atlas.aligner.gui.bdv.BdvMultislicePositionerView
import net.imglib2.realtransform.AffineTransform3D
import sc.fiji.bdvpg.viewer.bdv.supplier.DefaultBdvSupplier
import sc.fiji.bdvpg.viewer.bdv.supplier.SerializableBdvOptions
import javax.swing.SwingUtilities

def titled = { BdvMultislicePositionerView v -> SwingUtilities.getWindowAncestor(v.getBdvh().getViewerPanel())?.getTitle() ?: "" }
def views = objects.getObjects(BdvMultislicePositionerView).toSorted { titled(it).contains("(session closed)") } // live sessions first
def v = views.find { titled(it) == window_title } ?: views.find { titled(it).startsWith(window_title) }
def sessions = objects.getObjects(MultiSlicePositioner)
boolean opened = false
if (views.isEmpty() && sessions.size() == 1 && !java.awt.GraphicsEnvironment.isHeadless()) {
    // A session started without a window: open one on it, as ABBA - ABBA Start does
    v = new BdvMultislicePositionerView(sessions[0], new DefaultBdvSupplier(new SerializableBdvOptions()).get())
    opened = true
    Thread.sleep(2000) // laid out before it is framed
}
if (v == null) throw new IllegalArgumentException("No ABBA window titled '" + window_title + "'. ABBA windows: "
        + views.collect { "'" + titled(it) + "'" }.join(", "))

def slices = v.msp.getSlices()
if (slice_index >= slices.size()) throw new IllegalArgumentException("No slice " + slice_index + ": the session has "
        + slices.size() + " slices (0 to " + (slices.size() - 1) + ")")
def all = region_mm?.trim()?.equalsIgnoreCase("all")
double[] region = null
if (region_mm?.trim() && !all) {
    region = region_mm.trim().split("\\s*,\\s*").collect { it as double } as double[]
    if (region.length != 4) throw new IllegalArgumentException("region_mm: 'x,y,width,height' in mm, or 'all', not '" + region_mm + "'")
}
def indices = { String csv, int n -> csv.trim() == "*" ? (0..<n).toList() : csv.trim().equalsIgnoreCase("none") ? []
        : csv.trim().split("\\s*,\\s*").collect { it as int } }

/** Fits a box of the viewer's global coordinates (x, y, width, height) to the window, at z = 0 (positioning mode) */
def fit = { double x, double y, double w, double h ->
    def panel = v.getBdvh().getViewerPanel()
    double scale = 0.95 * Math.min(panel.getWidth() / w, panel.getHeight() / h)
    def t = new AffineTransform3D()
    t.scale(scale)
    t.translate(panel.getWidth() / 2.0 - scale * (x + w / 2), panel.getHeight() / 2.0 - scale * (y + h / 2), 0)
    panel.state().setViewerTransform(t)
    panel.requestRepaint()
}

try { SwingUtilities.invokeAndWait({
    if (mode == "review") v.setDisplayMode(BdvMultislicePositionerView.REVIEW_MODE_INT)
    if (mode == "positioning") v.setDisplayMode(BdvMultislicePositionerView.POSITIONING_MODE_INT)
    if (slice_index >= 0) v.navigateSlice(slices.get(slice_index))
    if (slice_channels?.trim()) {
        slices.each { SliceSources s ->
            def shown = indices(slice_channels, s.nChannels)
            (0..<s.nChannels).each { c -> v.setSliceChannelVisibility(s, c, shown.contains(c)) }
        }
    }
    if (atlas_channels?.trim()) {
        int n = v.getDisplayedAtlasSources().length // the label channel is not displayed
        def shown = indices(atlas_channels, n)
        (0..<n).each { c -> v.setAtlasChannelVisibility(c, shown.contains(c)) }
    }
    def current = v.getCurrentSlice()
    if (v.getDisplayMode() == BdvMultislicePositionerView.POSITIONING_MODE_INT && region == null && !slices.isEmpty()) {
        // The atlas sections in a row at y = 0, the slices below them: frame them together
        int i = slices.indexOf(current)
        def framed = all || i < 0 ? slices : slices.subList(Math.max(0, i - 2), Math.min(slices.size(), i + 3))
        def centers = framed.collect { v.getDisplayedCenter(it) }
        double x0 = centers.collect { it.getDoublePosition(0) }.min() - v.msp.sX / 2
        double x1 = centers.collect { it.getDoublePosition(0) }.max() + v.msp.sX / 2
        double y1 = Math.max(centers.collect { it.getDoublePosition(1) }.max(), 0) + v.msp.sY / 2
        fit(x0, -v.msp.sY / 2, x1 - x0, y1 + v.msp.sY / 2)
    } else {
        // The atlas section of the current slice, fitted to the window; then the region within it
        v.centerOnAtlas(current instanceof SliceSources ? v.msp.toAtlasZ(((SliceSources) current).getSlicingAxisPosition()) : v.msp.toAtlasZ(v.msp.sZ / 2.0))
        if (region != null) v.setViewRegionMm(region[0], region[1], region[2], region[3])
    }
} as Runnable) }
catch (java.lang.reflect.InvocationTargetException e) { throw e.getCause() } // what failed, not the wrapper
Thread.sleep(1500) // the window draws progressively: a picture taken at once would miss part of it

def current = v.getCurrentSlice()
boolean positioning = v.getDisplayMode() == BdvMultislicePositionerView.POSITIONING_MODE_INT
def keys = v.msp.getAtlas().getMap().getImagesKeys()
def visibleAtlas = (0..<v.getDisplayedAtlasSources().length).findAll { v.getAtlasChannelVisibility(it) }
        .collect { it + " (" + (it < keys.size() ? keys[it] : "channel " + it) + ")" }
view = (opened ? "Opened a window on the session (it had none); " : "") + (positioning ? "positioning" : "review") + " mode; current slice: " +
        (current instanceof SliceSources ? "#" + slices.indexOf(current) + " " + current.getName() + String.format(Locale.ROOT, " (z=%.3f mm)",
                v.msp.toAtlasZ(((SliceSources) current).getSlicingAxisPosition())) : "none") +
        "; framed: " + (region != null ? "region " + region_mm.trim() + " mm" : positioning ? (all ? "all the slices" : "the current slice and its neighbours") + ", with the atlas above" : "the whole atlas section") +
        "; atlas channels shown: " + visibleAtlas +
        (slice_channels?.trim() ? "; slice channels shown: " + slice_channels.trim() : "") + "."

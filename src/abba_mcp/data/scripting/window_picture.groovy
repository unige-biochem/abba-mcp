#@script(record="false")
#@ String (label = "Window title", value = "Aligning Big Brains and Atlases") window_title
#@output ij.ImagePlus picture
// A picture of one Fiji window as it is drawn, not of the screen: right when the window is covered, minimized behind
// other applications or the screen is locked, and never anything else. The bundle's abba_window_picture tool runs it.
// record="false": it only looks, so fiji_module_script leaves it out of the pipeline.
import java.awt.Dialog
import java.awt.Frame
import java.awt.Window
import java.awt.image.BufferedImage
import javax.swing.SwingUtilities

def title = { Window w -> w instanceof Frame ? ((Frame) w).getTitle() : w instanceof Dialog ? ((Dialog) w).getTitle() : null }
def frames = Window.getWindows().findAll { it.isDisplayable() && title(it) } // windows and dialogs
        .toSorted { title(it).contains("(session closed)") } // an ABBA window of a closed session last
def frame = frames.find { title(it) == window_title } ?: frames.find { title(it).startsWith(window_title) }
if (frame == null) throw new IllegalArgumentException("No window titled '" + window_title + "'. Open windows: "
        + frames.collect { "'" + title(it) + "'" }.join(", "))
BufferedImage image = new BufferedImage(frame.getWidth(), frame.getHeight(), BufferedImage.TYPE_INT_RGB)
SwingUtilities.invokeAndWait({ def g = image.createGraphics(); frame.printAll(g); g.dispose() } as Runnable)
picture = new ij.ImagePlus(title(frame), image)

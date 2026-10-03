#@script(record="false")
#@ String (label = "Window title", value = "Aligning Big Brains and Atlases") window_title
#@output ij.ImagePlus picture
// A picture of one Fiji window as it is drawn, not of the screen: right when the window is covered, minimized behind
// other applications or the screen is locked, and never anything else. The bundle's abba_window_picture tool runs it.
// record="false": it only looks, so fiji_module_script leaves it out of the pipeline.
import java.awt.Frame
import java.awt.image.BufferedImage
import javax.swing.SwingUtilities

def frames = Frame.getFrames().findAll { it.isDisplayable() && it.getTitle() }
def frame = frames.find { it.getTitle() == window_title } ?: frames.find { it.getTitle().startsWith(window_title) }
if (frame == null) throw new IllegalArgumentException("No window titled '" + window_title + "'. Open windows: "
        + frames.collect { "'" + it.getTitle() + "'" }.join(", "))
BufferedImage image = new BufferedImage(frame.getWidth(), frame.getHeight(), BufferedImage.TYPE_INT_RGB)
SwingUtilities.invokeAndWait({ def g = image.createGraphics(); frame.printAll(g); g.dispose() } as Runnable)
picture = new ij.ImagePlus(frame.getTitle(), image)

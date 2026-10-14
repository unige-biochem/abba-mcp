#@ sc.fiji.llm.mcp.MCPService mcp
#@ org.scijava.ui.UIService ui
#@ org.scijava.prefs.PrefService prefs
// Starts fiji-llm's MCP server; headless, keeps the JVM (and the server) alive until killed.
import sc.fiji.llm.mcp.MCPService

// The port abba-mcp waits on (9090, or ABBA_MCP_PORT). fiji-llm reads it from a preference shared by every Fiji of
// this user, which another Fiji may have left at another value: set it while the server starts, then put it back.
def port = System.getProperty("abba.mcp.port")
if (!mcp.isServerRunning()) {
    if (port) {
        def before = prefs.get(MCPService, MCPService.PORT_KEY, null)
        prefs.put(MCPService, MCPService.PORT_KEY, port as int)
        try { mcp.startServer() }
        finally { if (before == null) prefs.remove(MCPService, MCPService.PORT_KEY) else prefs.put(MCPService, MCPService.PORT_KEY, before) }
    } else {
        mcp.startServer()
    }
}
// For the server, which checks that Fiji listens where it waits
def home = System.getProperty("abba.mcp.home") ?: System.getProperty("java.io.tmpdir")
new File(home, "mcp-started.txt").text = "port=" + (port ?: mcp.getServerPort()) + " tools=" + mcp.getToolCount() + " headless=" + ui.isHeadless()
if (ui.isHeadless()) while (true) Thread.sleep(60000)

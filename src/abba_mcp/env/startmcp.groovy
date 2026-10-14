#@ sc.fiji.llm.mcp.MCPService mcp
#@ org.scijava.ui.UIService ui
#@ org.scijava.prefs.PrefService prefs
// Starts fiji-llm's MCP server; headless, keeps the JVM (and the server) alive until killed.
import sc.fiji.llm.mcp.MCPService

if (!mcp.isServerRunning()) {
    def port = System.getProperty("abba.mcp.port") // ABBA_MCP_PORT, for several bundles side by side (tests)
    if (port) {
        // The port is a preference shared by every Fiji of this user: set only while the server reads it
        def before = prefs.get(MCPService, MCPService.PORT_KEY, null)
        prefs.put(MCPService, MCPService.PORT_KEY, port as int)
        try { mcp.startServer() }
        finally { if (before == null) prefs.remove(MCPService, MCPService.PORT_KEY) else prefs.put(MCPService, MCPService.PORT_KEY, before) }
    } else {
        mcp.startServer()
    }
}
new File(System.getProperty("java.io.tmpdir"), "mcp-started.txt").text = "port=" + mcp.getServerPort() + " tools=" + mcp.getToolCount() + " headless=" + ui.isHeadless()
if (ui.isHeadless()) while (true) Thread.sleep(60000)

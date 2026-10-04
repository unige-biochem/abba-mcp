#@ sc.fiji.llm.mcp.MCPService mcp
#@ org.scijava.ui.UIService ui
// Starts fiji-llm's MCP server; headless, keeps the JVM (and the server) alive until killed.
if (!mcp.isServerRunning()) mcp.startServer()
new File(System.getProperty("java.io.tmpdir"), "mcp-started.txt").text = "port=" + mcp.getServerPort() + " tools=" + mcp.getToolCount() + " headless=" + ui.isHeadless()
if (ui.isHeadless()) while (true) Thread.sleep(60000)

#@ File (style = "directory") outDir
#@ String (value = "ch.epfl.biop.atlas") packagePrefix
#@ CommandService commands
#@output Integer written
// sextant: one Markdown file per command of the environment, in a tree that mirrors the menu,
// generated from the commands' own annotations (scijava-introspect, static: no initializer runs).
import ch.unige.biochem.scijava.introspect.CommandIntrospector
import groovy.json.JsonSlurper

def safe = { String s -> s.replaceAll('[\\\\/:*?"<>|]', '_').trim() }
def index = []
written = 0
commands.getCommands().findAll { it.className.startsWith(packagePrefix) }.sort { it.menuPath?.toString() ?: it.className }.each { info ->
    def cls
    try { cls = info.loadClass() } catch (Throwable t) { return }
    def d = null
    try { d = new JsonSlurper().parseText(CommandIntrospector.toJson(cls))[0] } catch (Throwable t) { }
    def dynamic = org.scijava.command.DynamicCommand.isAssignableFrom(cls)
    if (d == null || dynamic) { // scijava-introspect skips dynamic commands: use the module's own metadata
        d = [description: info.description ?: d?.description, output: [], input: []]
        info.inputs().each { item ->
            if (org.scijava.service.Service.isAssignableFrom(item.type) || org.scijava.Context.isAssignableFrom(item.type)) return
            if (item.visibility == org.scijava.ItemVisibility.MESSAGE) return
            def p = [name: item.name, type: item.type.simpleName, label: item.label, description: item.description]
            if (item.choices) p.choices = item.choices
            if (!item.required) p.required = false
            d.input << p
        }
        info.outputs().each { item -> d.output << [name: item.name, type: item.type.simpleName] }
        if (dynamic) d.description = (d.description ? d.description + "\n\n" : "") +
            "**Dynamic command**: its choices and defaults are computed when it starts. Call `fiji_module_describe` with its title to see them."
    }
    def menu = info.menuPath?.collect { it.name } ?: []
    def title = menu ? menu[-1] : cls.simpleName
    // Folder: the last menu level only (Align, Export, Inspect...): short paths, as Windows limits them to 260 characters
    def dir = menu.size() > 1 ? new File(outDir, safe(menu[-2]).replaceAll(/[()]/, "")) : new File(outDir, "_no_menu")
    dir.mkdirs()
    def md = new StringBuilder()
    md << "# ${title}\n\n"
    if (menu) md << "Menu: `${menu.join(' > ')}`  \n"
    md << "Class: `${cls.name}`\n\n"
    if (d.description) md << "${d.description}\n\n"
    def inputs = (d.input ?: []).findAll { !(it.type in ['Button']) }
    if (inputs) {
        md << "## Inputs\n\n"
        inputs.each { p ->
            md << "- `${p.name}` (${p.type})"
            if (p.label && p.label != p.name) md << " **${p.label}**"
            if (p.containsKey('default') && p.default != null && p.default.toString() != '') md << ", default `${p.default}`"
            if (p.choices) md << ", one of: " + p.choices.collect { "`${it}`" }.join(', ')
            if (p.required == false) md << ", optional"
            md << "\n"
            if (p.description) md << "  ${p.description}\n"
        }
        md << "\n"
    }
    def outputs = d.output ?: []
    if (outputs) {
        md << "## Outputs\n\n"
        outputs.each { p -> md << "- `${p.name}` (${p.type})" + (p.description ? ": ${p.description}" : "") + "\n" }
        md << "\n"
    }
    def f = new File(dir, safe(title) + ".md")
    f.text = md.toString()
    index << "- [${title}](${outDir.toPath().relativize(f.toPath()).toString().replace('\\', '/')})" + (d.description ? " - " + d.description.toString().replaceAll(/<[^>]*>/, ' ').replaceAll(/\s+/, ' ').take(110) : "")
    written++
}
new File(outDir, "INDEX.md").text = "# Commands of this environment (${packagePrefix}*)\n\nRun them by title with `fiji_module_run`. One file per command, in a folder named after its menu (Align, Export, Inspect...); the full menu path is in each file.\n\n" + index.join("\n") + "\n"

# Environment

What this server runs. Pinned: the same versions on every machine (see `env/jgo.toml` in the bundle).
If a command or an option you expect is missing, check here before assuming you got its name wrong.

| Component | Version |
|---|---|
| ABBA (ch.epfl.biop:ImageToAtlasRegister) | 0.23.1-SNAPSHOT |
| Atlases (ch.epfl.biop:atlas): Allen mouse CCFv3 / v3.1, Waxholm rat v4 / v4.2, BrainGlobe | 0.23.3-SNAPSHOT |
| BigDataViewer-Playground (sc.fiji:bigdataviewer-playground) | 0.23.1 |
| BIOP tools, Elastix wrapper (ch.epfl.biop:bigdataviewer-biop-tools) | 0.24.0 |
| Image loaders: Bio-Formats, OMERO, QuPath projects (ch.epfl.biop:bigdataviewer-image-loaders) | 0.23.2 |
| BigDataViewer core (sc.fiji:bigdataviewer-core) | 10.6.11 |
| Fiji (sc.fiji:fiji) | 2.18.0 |
| ImageJ 1.x (net.imagej:ij) | 1.54p |
| Appose (org.apposed:appose) | 0.12.0 |
| fiji-llm (MCP server) / fiji-modules (module tools) | 0.1.0-SNAPSHOT / 0.1.0-SNAPSHOT |
| Java | 21 (downloaded by jgo) |

Python tools, installed on first use through Appose (pixi), in their own environments:

| Tool | Version | First use |
|---|---|---|
| DeepSlice | 1.2.8 (TensorFlow 2.21.0, Python 3.12, CPU only) | large download (TensorFlow), several minutes |
| Elastix (itk-elastix) | 0.25.4, Python 3.11 | download, a few minutes |
| BrainGlobe atlas API | used for BrainGlobe atlases | atlases are downloaded on demand |

Not in this environment: QuPath itself (ABBA reads and writes QuPath projects, but QuPath is a separate
application), the ABBA Python package (abba_python).

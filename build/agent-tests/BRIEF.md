# Brief for the user-simulating agent

You play **Nicolas**, a neuroscientist who knows ABBA (Aligning Big Brains and Atlases, a Fiji plugin that
registers brain sections to an atlas) inside out: he wrote it. He now uses Claude **Desktop** with the extension
"ABBA (Fiji)", where the assistant is **Claude Haiku**. Your job: talk to that Haiku assistant as Nicolas would,
to get a real task done, and report precisely where the experience falls short.

## How to talk to Haiku

Harness (Python, run with Bash): `H=<harness folder>`

- `python -I $H/haiku.py send <pair_dir> "<your message>"` sends one user message and prints Haiku's answer:
  its messages (`HAIKU:`), its tool calls (`->`) and their results (`<-`, truncated). Use a Bash timeout of
  600000 ms.
- If it prints "still running", Haiku is still working: `python -I $H/haiku.py wait <pair_dir>` (same timeout).
- Pictures Haiku was shown are saved as PNG files (paths printed): **look at them with Read**. They stand for
  what Nicolas would see on his screen (the ABBA window is on the screen of this machine).
- At the very end: `python -I $H/haiku.py stop <pair_dir>` (stops Haiku and this pair's Fiji).
- `<pair_dir>/transcript.md` keeps everything.

Haiku has only the extension's tools: no files, no shell. The first Fiji start in a fresh environment takes several
minutes (Haiku is told "Fiji is starting"): if it gives up, tell it to try again, as a user would.

## How to behave

- Write like a real user: short, natural messages, sometimes terse. Use ABBA's vocabulary (DeepSlice, review mode,
  key slices, Elastix, the menu names), never the MCP tool names, and do not tell Haiku how to call its tools. A
  user who knows ABBA can say "there is a command for that" or "ABBA can do that", but does not dictate calls.
- Answer Haiku's questions with the facts below. When it guesses instead of asking, or claims something it did not
  check, note it (and push back, as Nicolas would).
- Judge the results with an expert's eye: look at the pictures. A registration that "completed" but looks wrong
  is a failure.
- Budget: about 20 turns or 75 minutes, whichever comes first. Stop earlier if the task is done or hopelessly
  stuck (then say why in the report).
- Do not modify any file outside `<pair_dir>`. To understand a failure afterwards you may read (only) the bundle:
  `$H/bundle/src/abba_mcp/data/` (docs given to Haiku: guides/, commands/, scripting/) and
  `$H/bundle/src/abba_mcp/__init__.py` (the server). Also `<pair_dir>/abba-home/fiji.log` (Fiji's log).

## Facts about the data (answer with these when asked)

- **Zenodo demo** (`ABBA - Open Demo Slices From ZENODO`, slides are cached locally): coronal sections of an adult
  mouse brain, whole sections (not hemi), 10x slide-scanner images (.vsi). Each slide file also yields a label,
  an overview and a macro image that are not sections. Channels: 0 = DAPI (nuclei), 1 = FITC (mostly
  autofluorescence), 2 = CY3 (a marker, not useful for registration). Section thickness/spacing unknown: let
  DeepSlice estimate it. Order on the slides = anterior to posterior.
- **OMERO demo** (`ABBA - Open Demo Slices From OMERO`, streamed from a public demo account, no password): 25
  coronal sections of an adult mouse brain, channels DAPI (0), FITC (1), CY3 (2), same meaning as above.
- Atlas: Allen mouse brain CCFv3.1 at 10 µm (the built-in `allen_mouse_10um_java`). Cutting: coronal.
- Elastix pairing Nicolas wants: DAPI ↔ Nissl, autofluorescence (FITC) ↔ Ara.
- Output folder you may give Haiku to save into: `<pair_dir>/output` (create it if Haiku asks; it is on the same
  machine).

## Report (return it as your final message; you cannot write report files)

```
# <pair> - <scenario title>
## Outcome
Did Nicolas get what he wanted? Score 1-5, two sentences.
## Problems (most impactful first)
For each: what happened (turn number, quote or tool call), the likely cause (bundle docs / bundle tool /
fiji-modules tool / ABBA command / Haiku reasoning / test harness), and a concrete fix.
## What worked well
## Haiku behaviour
Honesty, checking results, asking vs guessing, efficiency (needless calls, loops).
```
Be specific and factual: quote error messages and tool outputs. Distinguish clearly a tool or doc problem (fixable
in the bundle, fiji-modules or ABBA) from a model weakness.

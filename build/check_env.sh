#!/usr/bin/env bash
# Fails if the bundle's environment resolves other versions of ABBA's key dependencies than ABBA's pom declares,
# or if the bundle's version is not the ABBA version it pins.
# Coordinate order in jgo.toml decides transitive versions silently: this caught biop-tools 0.23.0 instead of 0.24.0.
# Usage: check_env.sh <dir with jgo.toml> <ABBA pom.xml>
set -euo pipefail
deps="$(cd "$1" && jgo --lenient --class-path-only info deplist 2>/dev/null)"
status=0
for a in bigdataviewer-biop-tools bigdataviewer-image-loaders bigdataviewer-playground; do
  want=$(grep -oE "<$a.version>[^<]+" "$2" | head -1 | cut -d'>' -f2)
  got=$(printf '%s\n' "$deps" | grep -oE ":$a:[^: ]+" | head -1 | cut -d: -f3)
  if [ "$want" = "$got" ]; then echo "ok   $a $got"; else echo "FAIL $a resolved $got, ABBA declares $want"; status=1; fi
done
# The bundle's version is ABBA's, plus "+N" for a re-release of the bundle alone (e.g. 0.24.0+1)
root="$(dirname "$0")/.."
abba=$(grep -oE 'ImageToAtlasRegister:[^"]+' "$1/jgo.toml" | cut -d: -f2)
manifest=$(grep -m1 -E '^\s*"version"' "$root/manifest.json" | cut -d'"' -f4)
project=$(grep -m1 -E '^version\s*=' "$root/pyproject.toml" | cut -d'"' -f2)
if [ "${manifest%%+*}" = "$abba" ] && [ "$project" = "$manifest" ]; then echo "ok   bundle version $manifest, ABBA $abba"
else echo "FAIL bundle version: manifest.json $manifest, pyproject.toml $project, ABBA $abba"; status=1; fi
exit $status

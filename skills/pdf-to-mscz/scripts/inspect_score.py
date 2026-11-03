#!/usr/bin/env python3
"""Read-only structural inventory of MusicXML/MuseScore files; Python 3.9+."""
import argparse
import json
from pathlib import Path, PurePosixPath
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

MAX_XML_BYTES = 64 * 1024 * 1024
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024
LIMITATIONS = [
    "Structural inventory only; not a schema validator or proof of musical accuracy.",
    "No pitch, rhythm, measure-duration, voice alignment, tie/slur or playback validation.",
    "Counts include grace notes and chord noteheads; they are not counts of timed events.",
    "Lyrics count only nonempty text nodes; melisma/extender lengths are not validated.",
    "Hidden-rest counts cover explicit rest visibility only, not inherited layout visibility.",
    "No comparison with a source PDF, visual rendering, or completeness assessment is performed.",
    "Part-to-staff associations are checked only when explicit staff IDs are present.",
]


def parse_xml(data):
    if len(data) > MAX_XML_BYTES:
        raise ValueError("XML exceeds the 64 MiB inspection limit")
    if b"<!ENTITY" in data.upper():
        raise ValueError("XML entity declarations are unsupported")
    root = ET.fromstring(data)
    for node in root.iter():
        node.tag = node.tag.rsplit("}", 1)[-1]  # Support default XML namespaces.
    return root


def text(node):
    return "".join(node.itertext()).strip() if node is not None else ""


def load_score(path):
    suffix = path.suffix.lower()
    if suffix not in {".xml", ".musicxml", ".mxl", ".mscx", ".mscz"}:
        raise ValueError("Supported suffixes: .xml .musicxml .mxl .mscx .mscz")
    if suffix not in {".mxl", ".mscz"}:
        if path.stat().st_size > MAX_XML_BYTES:
            raise ValueError("XML exceeds the 64 MiB inspection limit")
        return parse_xml(path.read_bytes()), {"zip_crc": "not_applicable"}
    with ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP member names make the container ambiguous")
        if sum(i.file_size for i in archive.infolist()) > MAX_ARCHIVE_BYTES:
            raise ValueError("Archive exceeds the 256 MiB uncompressed inspection limit")
        bad = archive.testzip()
        if bad:
            raise ValueError("ZIP CRC failure: " + bad)
        if "META-INF/container.xml" not in names:
            raise ValueError("Missing META-INF/container.xml; refusing to guess the main score")
        container = parse_xml(archive.read("META-INF/container.xml"))
        roots = container.findall("./rootfiles/rootfile")
        if suffix == ".mscz":
            selected = [n.get("full-path", "") for n in roots
                        if n.get("full-path", "").lower().endswith(".mscx")]
        else:
            typed = [n for n in roots if n.get("media-type") ==
                     "application/vnd.recordare.musicxml+xml"]
            selected = [n.get("full-path", "") for n in (typed or roots)
                        if n.get("full-path", "").lower().endswith((".xml", ".musicxml"))]
        if len(selected) != 1:
            raise ValueError("Container must identify exactly one main score; found " + str(selected))
        member = selected[0]
        if PurePosixPath(member).is_absolute() or ".." in PurePosixPath(member).parts:
            raise ValueError("Unsafe container score path: " + member)
        if member not in names:
            raise ValueError("Container references a missing score: " + member)
        if archive.getinfo(member).file_size > MAX_XML_BYTES:
            raise ValueError("Main score exceeds the 64 MiB inspection limit")
        return parse_xml(archive.read(member)), {
            "zip_crc": "ok", "main_member": member, "member_count": len(names)}


def signature_overview(measures, tags):
    result = []
    for index, measure in enumerate(measures, 1):
        for node in measure.iter():
            if node.tag in tags:
                result.append({"measure_index": index, "measure_number": measure.get("number"),
                               "kind": node.tag, "attributes": node.attrib,
                               "fields": [{"name": c.tag, "value": text(c),
                                           "attributes": c.attrib} for c in node]})
    return result


def count_notes(notes, lyrics, hidden):
    rests = sum(n.find("rest") is not None for n in notes)
    return {"noteheads": len(notes) - rests, "rests": rests,
            "note_or_rest_elements": len(notes), "nonempty_lyrics": sum(any(text(t) for t in l.findall("text")) for l in lyrics),
            "explicit_hidden_rests": hidden}


def musicxml(root, warnings):
    definitions = {p.get("id"): text(p.find("part-name"))
                   for p in root.findall("./part-list/score-part")}
    parts = []
    for part in root.findall("part"):
        measures = part.findall("measure")
        notes = [n for m in measures for n in m.findall("note")]
        staffs = {"1"}
        for declaration in part.findall("./measure/attributes/staves"):
            try:
                number = int(declaration.text)
                if number < 1 or number > 128:
                    raise ValueError()
                staffs.update(str(i) for i in range(1, number + 1))
            except (ValueError, TypeError):
                warnings.append("Invalid/unsupported staff count in part " + str(part.get("id")))
        for number in {n.findtext("staff", "1") for n in notes}:
            try:
                value = int(number)
                if not 1 <= value <= 128:
                    raise ValueError()
                if str(value) not in staffs:
                    warnings.append("Staff count inferred from note staff number in part " + str(part.get("id")))
                staffs.update(str(i) for i in range(1, value + 1))
            except (ValueError, TypeError):
                warnings.append("Invalid note staff number in part " + str(part.get("id")))
        counts = count_notes(notes, [l for n in notes for l in n.findall("lyric")],
                             sum(n.find("rest") is not None and n.get("print-object") == "no" for n in notes))
        parts.append({"id": part.get("id"), "name": definitions.get(part.get("id")),
                      "staff_count": len(staffs), "staff_numbers": sorted(staffs),
                      "measures": len(measures), **counts,
                      "keys_times_clefs": signature_overview(measures, {"key", "time", "clef"})})
        if not measures:
            warnings.append("Part has no measures: " + str(part.get("id")))
        if part.get("id") not in definitions:
            warnings.append("Part lacks a matching score-part definition: " + str(part.get("id")))
    if not parts:
        warnings.append("No score parts found")
    declared = set(definitions)
    actual = {p.get("id") for p in root.findall("part")}
    if None in declared or None in actual:
        warnings.append("Missing part ID")
    if declared - actual:
        warnings.append("Declared parts without music: " + str(sorted(map(str, declared - actual))))
    if len(actual) != len(parts):
        warnings.append("Duplicate part IDs")
    features = {n.tag for n in root.iter()} & {"time-modification", "tuplet", "grace", "backup", "forward", "unpitched"}
    if len({n.text for n in root.findall("./part/measure/note/voice")}) > 1:
        warnings.append("Multiple voices counted but not rhythmically validated")
    if features:
        warnings.append("Musical features counted but not validated: " + ", ".join(sorted(features)))
    return {"format": "MusicXML score-partwise", "title": text(root.find("work/work-title")) or
            text(root.find("movement-title")) or None, "part_count": len(parts),
            "staff_count": sum(p["staff_count"] for p in parts), "parts": parts}


def musescore(root, warnings):
    scores = [root] if root.tag == "Score" else root.findall("Score")
    if len(scores) != 1:
        raise ValueError("Expected exactly one top-level MuseScore Score")
    score = scores[0]
    if score.findall(".//Score"):
        warnings.append("Nested excerpt scores are excluded; only the top-level score is inspected")
    parts = [{"name": p.findtext("trackName") or text(p.find("Instrument/longName")),
              "declared_staff_count": len(p.findall("Staff")),
              "staff_ids": [s.get("id") for s in p.findall("Staff") if s.get("id")]}
             for p in score.findall("Part")]
    staves = []
    for staff in score.findall("Staff"):
        measures = staff.findall("Measure")
        notes = [n for m in measures for n in m.findall(".//Chord/Note")]
        rests = [n for m in measures for n in m.findall(".//Rest")]
        lyrics = [l for m in measures for l in m.findall(".//Lyrics")]
        staves.append({"id": staff.get("id"), "measures": len(measures),
                       "noteheads": len(notes), "rests": len(rests),
                       "note_or_rest_elements": len(notes) + len(rests),
                       "nonempty_lyrics": sum(any(text(t) for t in l.findall("text")) for l in lyrics),
                       "explicit_hidden_rests": sum(n.findtext("visible") == "0" for n in rests),
                       "keys_times_clefs": signature_overview(measures, {"KeySig", "TimeSig", "Clef"})})
        if not measures:
            warnings.append("Staff has no measures: " + str(staff.get("id")))
    ids = [s["id"] for s in staves]
    refs = [i for p in parts for i in p["staff_ids"]]
    mapping = "explicit_ids_match"
    if len(refs) != sum(p["declared_staff_count"] for p in parts) or any(i is None for i in ids):
        mapping = "unresolved_missing_ids"
        warnings.append("Part-to-staff mapping unresolved: explicit staff IDs are missing; sequential association is not validated")
    elif sorted(refs) != sorted(ids):
        mapping = "explicit_ids_mismatch"
        warnings.append("Explicit part-to-staff references do not match score staves")
    if sum(p["declared_staff_count"] for p in parts) != len(staves):
        warnings.append("Declared part staff count differs from musical staff count")
    if len(set(ids)) != len(ids):
        warnings.append("Duplicate staff IDs")
    if not parts or not staves:
        warnings.append("Missing part metadata or musical staves; counts may be incomplete")
    if any(len(m.findall("voice")) > 1 for s in score.findall("Staff") for m in s.findall("Measure")):
        warnings.append("Multiple voices counted but not rhythmically validated")
    features = {n.tag for s in score.findall("Staff") for n in s.iter()} & {
        "Tuplet", "location", "acciaccatura", "appoggiatura", "grace4", "grace8", "grace16",
        "grace32", "grace8after", "grace16after", "grace32after"}
    if features:
        warnings.append("Musical features counted but not validated: " + ", ".join(sorted(features)))
    title = text(score.find("metaTag[@name='workTitle']"))
    if not title:
        title = next((text(n.find("text")) for n in score.findall(".//VBox/Text")
                      if n.findtext("style", "").lower() == "title"), None)
    return {"format": "MuseScore", "version": root.get("version"), "title": title,
            "part_count": len(parts), "staff_count": len(staves), "part_staff_mapping": mapping,
            "parts": parts, "staves": staves}


def inspect(path):
    root, container = load_score(path)
    warnings = []
    if root.tag == "score-partwise":
        result = musicxml(root, warnings)
    elif root.tag in {"museScore", "Score"}:
        result = musescore(root, warnings)
    else:
        raise ValueError("Unsupported XML root: " + root.tag + "; score-timewise is not supported")
    units = result.get("staves", result["parts"])
    if len({u["measures"] for u in units}) > 1:
        warnings.append("Measure counts differ across parts/staves")
    if not result["title"]:
        warnings.append("No title found")
    result["totals"] = {k: sum(u[k] for u in units) for k in (
        "noteheads", "rests", "note_or_rest_elements", "nonempty_lyrics", "explicit_hidden_rests")}
    return {"status": "inspected", "input": str(path), "container": container,
            **result, "warnings": warnings, "limitations": LIMITATIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Prints JSON to stdout; never modifies or extracts input files. Exit 0 means inspection "
        "completed, not that the score is correct; exit 2 means inspection failed. ZIP inputs "
        "require an unambiguous META-INF/container.xml. Limits: 64 MiB XML / 256 MiB ZIP expanded."))
    parser.add_argument("score", type=Path, help=".musicxml/.xml/.mxl/.mscx/.mscz score")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    args = parser.parse_args()
    try:
        result = inspect(args.score)
        code = 0
    except (OSError, ValueError, ET.ParseError, BadZipFile, KeyError, RuntimeError, NotImplementedError, EOFError) as exc:
        result = {"status": "error", "input": str(args.score), "error": str(exc), "limitations": LIMITATIONS}
        code = 2
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return code


if __name__ == "__main__":
    sys.exit(main())

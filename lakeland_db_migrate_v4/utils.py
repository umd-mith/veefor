"""Helper function to deal with the mess of NAS paths."""
import re
from pathlib import Path

root_mapping: dict[str, str] = {
    "Assorted Jump Drives": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Audiovisual": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "City of College Park Documents": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Documents": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Lakeland High School Reunion Summer 2018": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "LCHP Oral Histories 2007-2013": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Maps": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Photos": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Publications": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Summer 2020 Oral Histories": "Projects/lakeland-digital-archive/object files/LCHP Accession 2021",
    "Audiovisual Materials Non-Oral History": "Projects/lakeland-digital-archive/object files/Files by Object Type-OLD-deprecate",
    "Projects": "",
}

ldt_path_regex = re.compile(r"[a-z0-9]{6}")
ldt_nas_root = Path(
    "Projects/lakeland-digital-archive/object files/2019 Digitization Event/Digitized Images"
)


def handle_paths(pathstrings: list[str]) -> list[str]:
    """Try to untangle the path data we receive."""
    deslashed = []
    normed = []

    for p in pathstrings:
        p = re.sub(r"[\s]{2,}", " ", p)
        unquoted_p = p.strip('"')
        if unquoted_p.startswith("/"):
            deslashed.append(unquoted_p[1:])
        else:
            deslashed.append(unquoted_p)

    if deslashed != [""]:
        pathobjs = [Path(p) for p in deslashed]
        for po in pathobjs:
            if po.parts[0] in root_mapping:
                full_path = Path(root_mapping[po.parts[0]])
                normed.append(full_path.joinpath(po))
            elif ldt_path_regex.match(po.parts[0]):
                normed.append(ldt_nas_root.joinpath(po))
            else:
                # 9 files have paths we can't do anything with
                pass
    return [n.as_posix() for n in normed]

"""Parse data_all.json (Django fixture) into plain Python dicts with resolved relationships."""

import json
from pathlib import Path


def load_data(fixture_path="data_all.json"):
    with open(fixture_path, encoding="utf-8") as f:
        fixture = json.load(f)

    labs, teams, researchers, projects = {}, {}, {}, {}

    for record in fixture:
        model = record["model"]
        pk = record["pk"]
        fields = record["fields"]

        if model == "directory.laboratory":
            labs[pk] = {"id": pk, **fields}
        elif model == "directory.team":
            teams[pk] = {"id": pk, **fields}
        elif model == "directory.researcher":
            researchers[pk] = {"id": pk, **fields}
        elif model == "directory.project":
            projects[pk] = {"id": pk, **fields}

    # Resolve team → lab
    for team in teams.values():
        team["lab"] = labs.get(team["lab"], {})

    # Resolve researcher → team, compute display fields
    for researcher in researchers.values():
        researcher["team"] = teams.get(researcher["team"], {})
        parts = [
            researcher.get("title", ""),
            researcher.get("first_name", ""),
            researcher.get("middle_initials", ""),
            researcher.get("last_name", ""),
        ]
        researcher["display_name"] = " ".join(p for p in parts if p).strip()
        # Email is omitted intentionally (spam risk on a public static page)
        researcher.pop("email", None)

        photo = researcher.get("photo", "")
        if photo and Path("media") / photo:
            photo_path = Path("media") / photo
            researcher["photo_url"] = f"/media/{photo}" if photo_path.exists() else None
        else:
            researcher["photo_url"] = None

    # Resolve project → researchers (M2M), compute logo URL
    for project in projects.values():
        project["contributors"] = [
            researchers[pk] for pk in project.get("members", []) if pk in researchers
        ]
        logo = project.get("logo", "")
        if logo:
            logo_path = Path("media") / logo
            project["logo_url"] = f"/media/{logo}" if logo_path.exists() else None
        else:
            project["logo_url"] = None

    # Attach projects to each researcher (reverse M2M)
    for researcher in researchers.values():
        researcher["projects"] = [
            p for p in projects.values() if researcher["id"] in p.get("members", [])
        ]

    return {
        "labs": labs,
        "teams": teams,
        "researchers": sorted(researchers.values(), key=lambda r: r.get("last_name", "")),
        "projects": list(projects.values()),
    }


if __name__ == "__main__":
    data = load_data()
    print(f"{len(data['researchers'])} researchers")
    print(f"{len(data['teams'])} teams")
    print(f"{len(data['projects'])} projects")
    print(f"{len(data['labs'])} labs")

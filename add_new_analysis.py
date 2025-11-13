#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
from datetime import date

import requests


def get_info(inspire_id: str, doi: str) -> dict[str, str]:
    """Extract information"""
    entry = {}
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()
        metadata = data.get("message", {})
        title = metadata.get("title", ["N/A"])[0]
        print("Title:", title)
        entry["name"] = title
    else:
        raise ValueError(f"DOI not found or not in Crossref: {response.status_code}")

    url = f"https://inspirehep.net/api/literature/{inspire_id}"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()["metadata"]
        print("\nINSPIRE Record:")
        print("Title:", data["titles"][0]["title"])
        print("DOI:", data.get("dois", [{}])[0].get("value", "N/A"))
        print("arXiv ID:", data.get("arxiv_eprints", [{}])[0].get("value", "N/A"))
        print("Abstract:", data["abstracts"][0]["value"])
    else:
        raise ValueError(
            f"Can not access INSPIRE record: {response.status_code}"
            f"Please check: {url}"
        )

    doi = doi.replace("doi.org/", "").replace("https://", "")
    entry.update({"path": doi})
    return entry


def main(args):

    with open("analyses.json", "r") as f:
        analyses = json.load(f)

    # Look for existing inspire ids
    loc = next(
        (
            idx
            for idx, a in enumerate(analyses["analyses"])
            if a["inspire_id"] == args.INSPIRE
        ),
        None,
    )

    if loc is None:
        analyses["analyses"].append(
            {
                "inspire_id": args.INSPIRE,
                "implementations": [get_info(args.INSPIRE, args.DOI)],
            }
        )
    else:
        analyses["analyses"][loc]["implementations"].append(
            get_info(args.INSPIRE, args.DOI)
        )

    loc = next(
        (
            idx
            for idx, a in enumerate(analyses["analyses"])
            if a["inspire_id"] == args.INSPIRE
        ),
        None,
    )

    analyses["date_created"] = date.today().strftime("%Y-%m_%d")
    with open("analyses_new.json", "w") as f:
        json.dump(analyses, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add new analysis to the Ma5 analyses stack"
    )
    info = parser.add_argument_group("Information")
    info.add_argument(
        "--inspire",
        required=True,
        type=str,
        help="Inspire HEP ID of the ",
        dest="INSPIRE",
    )
    info.add_argument(
        "--doi",
        required=True,
        type=str,
        help="Short DOI link e.g. 10.14428/DVN/31JVGJ",
        dest="DOI",
    )

    args = parser.parse_args()
    main(args)

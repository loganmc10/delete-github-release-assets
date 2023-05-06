#!/usr/bin/env python3
import requests
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete old GitHub release assets.")
    parser.add_argument("-o", "--owner", type=str, help="Owner")
    parser.add_argument("-r", "--repo", type=str, help="Repo")
    parser.add_argument("-t", "--token", type=str, help="GitHub API Token")
    parser.add_argument(
        "-k",
        "--keep",
        type=int,
        default=3,
        help="How many releases to leave untouched. Default=3",
    )
    args = parser.parse_args()
    headers = {"Authorization": f"Bearer {args.token}"}

    assets = []
    release_counter = 0
    next_url = f"https://api.github.com/repos/{args.owner}/{args.repo}/releases"
    while next_url:
        r = requests.get(
            next_url,
            timeout=10,
            headers=headers,
        )
        r.raise_for_status()
        try:
            next_url = r.links["next"]["url"]
        except KeyError:
            next_url = ""
        for release in r.json():
            if release_counter >= args.keep:
                for asset in release["assets"]:
                    assets.append(asset["url"])
            else:
                print(f"skipped {release['tag_name']}")
            release_counter += 1
    for asset in assets:
        r = requests.delete(asset, timeout=10, headers=headers)
        r.raise_for_status()
        print(f"Deleted {asset}")


if __name__ == "__main__":
    main()

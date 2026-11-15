"""Daily snapshot of GitHub numbers into PostHog, kept apart from real usage.

Stars and forks are interest, release downloads are downloads; neither is usage.
Usage comes from the anonymous events in skills/punchcutter/scripts/pc/telemetry.py.
GitHub keeps traffic (views, clones, referrers) for only 14 days, so this records it
every day. Traffic needs a token with push access in the TRAFFIC_TOKEN secret;
without it the public numbers are still recorded.
"""
import datetime
import json
import os
import urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "byrishi/punchcutter")
KEY = "phc_OP89N6nuHWu48k3n7j2fhFcA2y51GODeJGMJgRZgPbv"
TOKEN = os.environ.get("TRAFFIC_TOKEN") or os.environ.get("GITHUB_TOKEN", "")


def gh(path, auth=True):
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}{path}", headers={"Accept": "application/vnd.github+json"})
    if auth and TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print(f"skip {path}: {e}")
        return None


def send(event, props):
    body = {"api_key": KEY, "event": event, "distinct_id": f"github:{REPO}",
            "properties": {"app": "punchcutter", "source": "github", "$process_person_profile": False, **props}}
    req = urllib.request.Request("https://us.i.posthog.com/i/v0/e/", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=20).read()


def main():
    repo = gh("", auth=False) or {}
    rels = gh("/releases?per_page=100", auth=False) or []
    downloads = {a["name"]: a["download_count"] for r in rels for a in r.get("assets", [])}
    day = datetime.date.today().isoformat()
    props = dict(day=day, stars=repo.get("stargazers_count"), forks=repo.get("forks_count"), watchers=repo.get("subscribers_count"),
                 open_issues=repo.get("open_issues_count"), release_downloads_total=sum(downloads.values()),
                 skill_downloads_total=sum(v for k, v in downloads.items() if k.endswith(".skill")))
    views, clones, refs = gh("/traffic/views"), gh("/traffic/clones"), gh("/traffic/popular/referrers")
    if views:
        last = (views.get("views") or [{}])[-1]
        props.update(views_14d=views.get("count"), visitors_14d=views.get("uniques"), views_yesterday=last.get("count"), visitors_yesterday=last.get("uniques"))
    if clones:
        props.update(clones_14d=clones.get("count"), cloners_14d=clones.get("uniques"))
    send("pc_github_daily", props)
    for r in refs or []:
        send("pc_github_referrer", dict(day=day, referrer=r["referrer"], views_14d=r["count"], visitors_14d=r["uniques"]))
    print(json.dumps(props, indent=1))


if __name__ == "__main__":
    main()

# Activity artwork

The README combines the restored ASCII hero with a contribution snake and custom SVG activity cards. Generated output lives on `profile-assets`; source and the scheduled workflow live on `main`. Refresh commits use the bot's actual dates and do not add commits to the default branch.

## Credential setup

Create a classic personal access token belonging to AssilBelhouen with only **read:user**. Save it as the repository Actions secret **PROFILE_STATS_TOKEN**. Choose an expiry and renew the secret before it expires. Do not paste it in an issue, commit, local configuration, or chat. No repository write scope is needed on this credential.

GitHub documents `read:user` for private contribution aggregates in its [GraphQL ContributionsCollection reference](https://docs.github.com/en/graphql/reference/users). Private contribution visibility and API restrictions can affect the returned counts. This credential does not grant access to private repository contents. The separate built-in workflow token publishes artwork with `contents: write` for this profile repository only.

## Schedule and manual refresh

The workflow runs daily at **06:17 Africa/Lagos** (`17 5 * * *` UTC). Open **Actions → Refresh profile activity → Run workflow** to refresh immediately or after rotating the secret. The workflow must exist on `main`.

[GitHub schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) can be delayed or dropped under load. Public repository schedules can be disabled after 60 days without activity; re-enable the workflow in Actions when necessary. The printed last successful refresh exposes stale artwork. GitHub's image proxy may also cache successful output briefly.

## What the numbers mean

- **Contributions:** GitHub's contribution calendar total for the rolling calendar year ending at refresh time. Eligible private contributions are already included; restricted contributions are never added again.
- **Commits, pull requests, reviews:** totals GitHub classifies and exposes to the authenticated API viewer. Restricted private activity may lack a type breakdown, so these cards do not claim exhaustive private counts.
- **Restricted:** the API's unclassified activity count, printed separately for transparency. It is not a second contribution total.

These are GitHub contribution counts, subject to eligibility, attribution, indexing and visibility rules—not every local commit or Git operation. Dates and the reporting window use UTC. Private names, repository IDs, payloads and API errors are not persisted. The accessible Markdown report contains the same aggregates as the SVG cards. Calendar day totals are visible in the snake, as in a contribution graph.

## Failure and publication

Missing/expired credentials, invalid API responses or snake generation failure stop the workflow before publishing. Existing artwork remains intact. Publication stages the complete output together, uses an ordinary push, and commits only changed files. Concurrent runs are serialized; a conflicting asset-branch push fails rather than overwriting it. No pull-request trigger receives the secret.

Dependencies are pinned: Python 3.12.14, actions/checkout `11d5960a326750d5838078e36cf38b85af677262`, actions/setup-python `a26af69be951a213d495a4c3e4e4022e16d87065`, and [Platane/snk](https://github.com/Platane/snk/tree/d8f6715049803e982ee5ff501b6b9b7d5deeb09b) `d8f6715049803e982ee5ff501b6b9b7d5deeb09b`. Review upstream changes before updating pins. The snake action receives the read-only activity token, never the write token. The publisher disables checkout credential persistence and supplies its write credential only to Git over HTTPS.

## Local checks

```sh
python -m unittest discover -s tools -p 'test_*.py'
bash -n tools/publish_activity.sh
```

Tests cover aggregate totals without double-counting, privacy filtering, missing credentials, API failures, invalid data, ownership, leap-day windows and unchanged rendering. A successful live workflow is required to validate real API authentication and snake generation.

## Reconstructed history

Manual profile commit author dates have been reconstructed as July 1, 2026 in Africa/Lagos, ordered by time. Actual committer dates, authors, messages and prior content were preserved during the rewrite. The first published history is recoverable from a local Git bundle outside the repository. Future automatic output commits retain actual dates.

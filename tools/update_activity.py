"""Read aggregate GitHub activity and render self-contained terminal SVGs.

Never persist API responses, tokens, repository identities, or contribution details.
"""
import argparse
import datetime as dt
import html
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

LOGIN = 'AssilBelhouen'
QUERY = '''query Activity($login: String!, $from: DateTime!, $to: DateTime!) {
  viewer { login }
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      startedAt endedAt restrictedContributionsCount
      totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions
      contributionCalendar { totalContributions }
    }
  }
}'''

class ActivityError(Exception):
    pass

def window(now):
    # A calendar year, including leap-day handling, within GitHub's one-year limit.
    try:
        start = now.replace(year=now.year-1)
    except ValueError:
        start = now.replace(year=now.year-1, day=28)
    return start, now

def stamp(value):
    return value.astimezone(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def fetch_activity(token, start, end, opener=urllib.request.urlopen):
    if not token:
        raise ActivityError('PROFILE_STATS_TOKEN is missing. Add the repository Actions secret.')
    request = urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query': QUERY, 'variables': {'login': LOGIN, 'from': stamp(start), 'to': stamp(end)}}).encode(),
        headers={'Authorization': 'Bearer '+token, 'Content-Type': 'application/json', 'User-Agent': 'Assil-profile-activity'})
    try:
        with opener(request, timeout=30) as response:
            scopes = response.headers.get('X-OAuth-Scopes', '')
            # Classic PATs explicitly advertise scopes; require the documented private-count scope.
            if scopes and not {'read:user', 'user'}.intersection(s.strip() for s in scopes.split(',')):
                raise ActivityError('Token lacks read:user permission for private contribution aggregates.')
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        raise ActivityError(f'GitHub request failed (HTTP {error.code}); check token expiry and access.') from None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        raise ActivityError('GitHub activity request failed; previous artwork was retained.') from None
    return normalize(payload)

def normalize(payload):
    if payload.get('errors'):
        raise ActivityError('GitHub GraphQL returned an error; previous artwork was retained.')
    try:
        if payload['data']['viewer']['login'].lower() != LOGIN.lower():
            raise ActivityError('The stats token must belong to AssilBelhouen.')
        c = payload['data']['user']['contributionsCollection']
        counts = {
            'contributions': c['contributionCalendar']['totalContributions'],
            'commits': c['totalCommitContributions'],
            'pull_requests': c['totalPullRequestContributions'],
            'reviews': c['totalPullRequestReviewContributions'],
            'restricted': c['restrictedContributionsCount'],
        }
        if any(type(v) is not int or v < 0 for v in counts.values()):
            raise ActivityError('GitHub returned invalid activity counts.')
        # Calendar total already includes eligible restricted activity. Never add it again.
        return counts
    except (KeyError, TypeError):
        raise ActivityError('GitHub returned incomplete activity data.') from None

def svg(counts, start, end, mobile=False):
    width, height = (600, 460) if mobile else (1200, 270)
    esc = html.escape
    period = f'{start:%Y-%m-%d} to {end:%Y-%m-%d} UTC'
    state = f'LAST SYNC / {stamp(end)}' if counts is not None else 'AWAITING / PROFILE_STATS_TOKEN'
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
      '<title id="title">Assil GitHub activity, past year</title>',
      '<desc id="desc">'+esc('Private activity is aggregate-only. Typed totals include only activity the API classifies. '+period+'. '+state)+'</desc>',
      '<style>@keyframes breathe{0%,100%{opacity:.3}50%{opacity:.9}}.signal{animation:breathe 4s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.signal{animation:none}}</style>',
      f'<rect width="{width}" height="{height}" rx="18" fill="#070A08"/>',
      f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="none" stroke="#253B2F"/>',
      '<circle class="signal" cx="28" cy="29" r="4" fill="#00FF88"/>',
      '<g font-family="monospace">',
      '<text x="42" y="34" fill="#00FF88" font-size="14">ACTIVITY / PAST YEAR</text>',
      f'<text x="24" y="61" fill="#A6B7AC" font-size="13">{period}</text>']
    labels = [('contributions','CONTRIBUTIONS'), ('commits','COMMITS*'), ('pull_requests','PULL REQUESTS*'), ('reviews','REVIEWS*')]
    for i,(key,label) in enumerate(labels):
        x = 24 + (i%2)*280 if mobile else 24+i*290
        y = 83+(i//2)*133 if mobile else 83
        value = f'{counts[key]:,}' if counts is not None else '\u2014'
        parts += [f'<rect x="{x}" y="{y}" width="{262 if mobile else 272}" height="113" rx="10" fill="#0D1410" stroke="#253B2F"/>',
          f'<text x="{x+18}" y="{y+27}" fill="#A6B7AC" font-size="12">{label}</text>',
          f'<text x="{x+18}" y="{y+82}" fill="#F5FFF8" font-size="43">{value}</text>']
    fy = 370 if mobile else 221
    parts += [f'<text x="24" y="{fy}" fill="#A6B7AC" font-size="12">* API-classified totals; restricted breakdown may be hidden.</text>',
      f'<text x="24" y="{fy+23}" fill="#A6B7AC" font-size="12">{esc(state)}</text>']
    if counts is not None:
        parts.append(f'<text x="24" y="{fy+45}" fill="#A6B7AC" font-size="12">Unclassified restricted contributions: {counts["restricted"]:,}</text>')
    parts.append('</g></svg>')
    return '\n'.join(parts)+'\n'

def render(directory, counts, start, end):
    directory.mkdir(parents=True, exist_ok=True)
    outputs = {'stats.svg': svg(counts,start,end), 'stats-mobile.svg': svg(counts,start,end,True)}
    if counts is None:
        text = '# Activity totals\n\nAwaiting the PROFILE_STATS_TOKEN Actions secret. No live counts have been published.\n'
    else:
        text = f'# Activity totals\n\nPeriod: {start:%Y-%m-%d} to {end:%Y-%m-%d} UTC. Last successful refresh: {stamp(end)}.\n\n'
        text += '| Metric | Count |\n|---|---:|\n'+''.join(f'| {k.replace("_"," ").title()} | {v:,} |\n' for k,v in counts.items())
        text += '\nContribution calendar totals already include eligible private activity. Restricted contributions are not added a second time. Commits, pull requests and reviews cover API-classified activity; restricted activity cannot necessarily be separated into those types. These are GitHub contribution counts, not every Git operation.\n'
    outputs['activity.md'] = text
    changed = 0
    for name, content in outputs.items():
        path = directory/name
        if not path.exists() or path.read_text(encoding='utf-8') != content:
            path.write_text(content, encoding='utf-8')
            changed += 1
    return changed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--placeholder', action='store_true', help='Create honestly labeled initial artwork without live counts.')
    args = parser.parse_args()
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    start,end = window(now)
    try:
        counts = None if args.placeholder else fetch_activity(os.environ.get('PROFILE_STATS_TOKEN',''),start,end)
        changed = render(args.output, counts, start, end)
    except ActivityError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f'Activity artwork ready: {changed} changed files. No private identifiers persisted.')
    return 0

if __name__ == '__main__':
    sys.exit(main())

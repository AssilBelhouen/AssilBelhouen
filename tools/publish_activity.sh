#!/usr/bin/env bash
set -euo pipefail
# Separate token and credential scope: only this step gets repository write access.
for asset in stats.svg stats-mobile.svg contribution-snake.svg contribution-snake-dark.svg activity.md; do
  test -s "generated/$asset"
done
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0=http.https://github.com/.extraheader
export GIT_CONFIG_VALUE_0="AUTHORIZATION: basic $(printf 'x-access-token:%s' "$GH_TOKEN" | base64 -w0)"
trap 'unset GIT_CONFIG_VALUE_0 GH_TOKEN' EXIT
git clone --quiet --single-branch --branch profile-assets "https://github.com/$GH_REPOSITORY.git" published
cp generated/*.svg generated/activity.md published/
cd published
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add stats.svg stats-mobile.svg contribution-snake.svg contribution-snake-dark.svg activity.md
if git diff --cached --quiet; then
  echo 'Activity assets are unchanged.'
else
  git commit -m 'Refresh aggregate GitHub activity artwork'
  git push origin HEAD:profile-assets
fi

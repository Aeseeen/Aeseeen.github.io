#!/usr/bin/env bash
# =============================================================================
#  deploy.sh — one-shot push + Pages enable
#
#  Ginagamit ito ng agent para i-push ang portfolio sa GitHub.
#  Hinihingi ang token mula sa environment variable, HINDI ito ini-store.
#
#  GAMIT:
#     GITHUB_TOKEN=xxx GITHUB_USER=yyy REPO_NAME=zzz bash deploy.sh
# =============================================================================
set -euo pipefail

: "${GITHUB_TOKEN:?Kailangan ang GITHUB_TOKEN}"
: "${GITHUB_USER:?Kailangan ang GITHUB_USER}"
: "${REPO_NAME:=${GITHUB_USER}.github.io}"

API="https://api.github.com"
REPO_DIR="/home/user/portfolio"

echo "==> Nag-a-authenticate..."
WHO=$(curl -s -H "Authorization: Bearer ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github+json" \
            "${API}/user" | python3 -c "import sys,json; print(json.load(sys.stdin).get('login',''))" 2>/dev/null || echo "")

if [ -z "$WHO" ]; then
  echo "❌ ERROR: Hindi tinanggap ang token — hindi ito makakuha ng user info."
  echo "   Karaniwang dahilan: (1) naka-set sa 'Public repositories' ang"
  echo "   Repository access — kailangan 'Only select repositories',"
  echo "   (2) wala pang naidagdag na permission sa Repository permissions,"
  echo "   (3) mali ang kopya ng token."
  echo "   Tsekan: (a) tama ba ang pagkakopya, (b) hindi pa expired,"
  echo "   (c) may 'Metadata: Read' permission ang fine-grained token."
  exit 1
fi
echo "✅ Naka-login bilang: ${WHO}"

if [ "$WHO" != "$GITHUB_USER" ]; then
  echo "❌ ERROR: Ang token ay para kay '${WHO}', pero ang sinabi mo ay '${GITHUB_USER}'."
  exit 1
fi

# --- 1. Gumawa ng repo kung wala pa
echo "==> Tinitignan kung may repo nang ${REPO_NAME}..."
HTTP=$(curl -s -o /dev/null -w "%{http_code}" \
            -H "Authorization: Bearer ${GITHUB_TOKEN}" \
            "${API}/repos/${GITHUB_USER}/${REPO_NAME}")

if [ "$HTTP" = "404" ]; then
  echo "==> Walang repo. Ginagawa..."
  CREATE=$(curl -s -X POST \
    -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    "${API}/user/repos" \
    -d "{\"name\":\"${REPO_NAME}\",\"description\":\"Portfolio — aviation maintenance x compliance automation\",\"private\":false,\"auto_init\":false}")
  echo "$CREATE" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if 'full_name' in d: print('✅ Nagawa:', d['full_name'])
else: print('❌ Hindi nagawa:', d.get('message'), d.get('errors',''))
" 
elif [ "$HTTP" = "200" ]; then
  echo "==> Umiiral na ang repo. Gagamitin na lang."
else
  echo "⚠️  Hindi inaasahang sagot ($HTTP). Susubukan pa rin."
fi

# --- 2. Ayusin ang site URL sa files
SITE_URL="https://${GITHUB_USER}.github.io"
[ "$REPO_NAME" != "${GITHUB_USER}.github.io" ] && SITE_URL="https://${GITHUB_USER}.github.io/${REPO_NAME}"

cd "$REPO_DIR"
sed -i "s|content=\"\[YOUR-PORTFOLIO-URL\]\"|content=\"${SITE_URL}\"|" index.html 2>/dev/null || true
sed -i "s|\[YOUR-PORTFOLIO-URL\]|${SITE_URL}|g" README.md 2>/dev/null || true
sed -i "s|\[YOUR-HANDLE\]|${GITHUB_USER}|g" index.html README.md 2>/dev/null || true
echo "==> Site URL: ${SITE_URL}"

# --- 3. Commit at push
[ -d .git ] || { git init -q; git checkout -q -b main; }
git add -A
git -c user.email="${GITHUB_USER}@users.noreply.github.com" \
    -c user.name="${GITHUB_USER}" commit -q -m "Deploy portfolio" || echo "==> Walang pagbabago."

git remote remove origin 2>/dev/null || true
# token sa URL: hindi ito naka-save sa .git/config dahil pinalitan agad pagkatapos
git remote add origin "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"
git push -u origin main --force -q
git remote set-url origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
echo "✅ Naka-push."

# --- 4. Buksan ang GitHub Pages
echo "==> Binubuhay ang GitHub Pages..."
PAGES=$(curl -s -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  "${API}/repos/${GITHUB_USER}/${REPO_NAME}/pages" \
  -d "{\"source\":{\"branch\":\"main\",\"path\":\"/\"}}")

echo "$PAGES" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('html_url'): print('✅ Pages ON:', d['html_url'])
else: print('⚠️  Pages:', d.get('message','di-ma-enable sa API — i-toggle sa Settings > Pages'))
"

echo
echo "=============================================="
echo "  SITE:       ${SITE_URL}"
echo "  REPO:       https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "=============================================="

#!/usr/bin/env bash
# =============================================================================
#  push-to-github.sh
#  Ilalagay ang portfolio sa GitHub mo — isang beses lang ito tatakbo.
#
#  PAANO GAMITIN:
#    1. Palitan ang GITHUB_USER sa ibaba ng totoong username mo
#    2. Piliin ang REPO_NAME (tingnan ang note sa baba)
#    3. bash push-to-github.sh
#
#  KAILANGAN:  git installed, at isang GitHub Personal Access Token (tingnan
#              ang SETUP-GITHUB.md para sa kung paano gumawa nito)
# =============================================================================
set -euo pipefail

# ----------------------------- PALITAN ITO -----------------------------------
GITHUB_USER="[YOUR-USERNAME]"

# PILIIN ANG ISA:
#   "<username>.github.io"  --> site mo ay nasa  https://<username>.github.io
#                               (mas malinis, ito ang recommended para sa CV)
#   "portfolio"             --> site mo ay nasa  https://<username>.github.io/portfolio
REPO_NAME="${GITHUB_USER}.github.io"
# -----------------------------------------------------------------------------

if [ "$GITHUB_USER" = "[YOUR-USERNAME]" ]; then
  echo "STOP: palitan mo muna ang GITHUB_USER sa script na ito."
  exit 1
fi

echo "==> Repo:  github.com/${GITHUB_USER}/${REPO_NAME}"

# --- 1. Siguraduhing nasa tamang folder
if [ ! -f index.html ]; then
  echo "STOP: walang index.html dito. Patakbuhin mo ito sa loob ng portfolio folder."
  exit 1
fi

# --- 2. Palitan ang OG:url placeholder (kung meron pa)
SITE_URL="https://${GITHUB_USER}.github.io"
if [ "$REPO_NAME" != "${GITHUB_USER}.github.io" ]; then
  SITE_URL="https://${GITHUB_USER}.github.io/${REPO_NAME}"
fi
sed -i "s|content=\"\[YOUR-PORTFOLIO-URL\]\"|content=\"${SITE_URL}\"|" index.html 2>/dev/null || true
sed -i "s|\[YOUR-PORTFOLIO-URL\]|${SITE_URL}|g" README.md 2>/dev/null || true
echo "==> Naitakda ang site URL sa: ${SITE_URL}"

# --- 3. Git init kung wala pa
if [ ! -d .git ]; then
  git init -q
  git branch -M main 2>/dev/null || git checkout -q -b main
fi

git add -A
git -c user.email="${GITHUB_USER}@users.noreply.github.com" \
    -c user.name="${GITHUB_USER}" \
    commit -q -m "Update portfolio" || echo "==> Walang bagong pagbabago."

# --- 4. Gumawa ng repo sa GitHub at i-push
#         (kailangan ng token; ilalagay mo ito kapag tinanong)
echo
echo "==> Pagtatanungin ka ng GitHub username at password."
echo "    PASSWORD = ang Personal Access Token mo (HINDI ang GitHub password mo)."
echo

git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "==> Kailangan mo pang gumawa ng EMPTY na repo sa GitHub bago mag-push:"
echo "    https://github.com/new"
echo "    Repository name : ${REPO_NAME}"
echo "    Visibility      : Public"
echo "    HUWAG mong tsekan ang 'Add a README file'"
echo
read -rp "Nagawa mo na ba ang repo? Pindutin ang Enter para magpatuloy..."

git push -u origin main

echo
echo "=============================================================="
echo "  TAPOS. Naka-push na sa GitHub."
echo "=============================================================="
echo
echo "  Site        : ${SITE_URL}"
echo "  Repository  : https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo
echo "  HAKBANG SUSUNOD — buhayin ang website:"
echo "    1. Buksan ang repository settings:"
echo "       https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages"
echo "    2. Sa 'Source', piliin ang:  Deploy from a branch"
echo "    3. Branch: main   |   Folder: / (root)   |   I-save"
echo "    4. Maghintay ng 1-2 minuto, tapos buksan ang site."
echo
echo "  Puwede nang i-paste ang URL na ito sa CV mo sa lugar ng"
echo "  [YOUR-PORTFOLIO-URL]:"
echo "    ${SITE_URL}"
echo

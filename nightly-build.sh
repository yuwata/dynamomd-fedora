#!/bin/bash

CMD=${0##*/}
SOURCE_DIR=$(cd $(dirname $0) && pwd)
REPO_NAME=${SOURCE_DIR##*/}
REPO_DIR=${HOME}/git/DynamO

HASH_OLD=$(grep -e '^[%#]global gitcommit' ${SOURCE_DIR}/${REPO_NAME}.spec | awk '{ print $3 }')
if [[ -z $HASH_OLD ]]; then
    echo 'error: cannot obtain old commit hash.' >&2
    exit 1
fi

if ! git -C $REPO_DIR fetch upstream --prune; then
    echo 'error: `git fetch upstream --prune` failed.' >&2
    exit 11
fi

if ! HASH_NEW=$(git -C $REPO_DIR show-ref --hash refs/remotes/upstream/master); then
    echo 'error: `git show-ref` failed.' >&2
    exit 12
fi

if [[ "$HASH_NEW" == "$HASH_OLD" ]]; then
    echo 'info: not necessary to update spec file.' >&2
    exit
fi

HASH_OLD_SHORT=${HASH_OLD:0:7}
HASH_NEW_SHORT=${HASH_NEW:0:7}

VERSION=$(grep -e '^Version:' ${SOURCE_DIR}/${REPO_NAME}.spec | awk '{ print $2 }')
if [[ -z $VERSION ]]; then
    echo 'error: cannot obtain version number.' >&2
    exit 13
fi

RELEASE_OLD=$(grep -e '^Release:' ${SOURCE_DIR}/${REPO_NAME}.spec | sed -e 's/^Release:[[:space:]]*//; s/%.*$//;')
if [[ -z $RELEASE_OLD ]]; then
    echo 'error: cannot obtain old release number.' >&2
    exit 14
fi

RELEASE_NEW=$(( $RELEASE_OLD + 1 ))
if [[ -z $RELEASE_NEW ]]; then
    echo 'error: cannot increment release number.' >&2
    exit 15
fi

WEEKDAY=$(date "+%a")
MONTH=$(date "+%b")
DAY=$(date "+%d")
YEAR=$(date "+%Y")

CHANGE_LOG="- Update to latest git snapshot ${HASH_NEW}\n"
COMMIT_LOG="Update to latest git snapshot ${HASH_NEW}\n\n"

sed -e '/^[%#]global gitcommit/ { s/^#/%/; s/'${HASH_OLD}'/'${HASH_NEW}'/ }' \
    -e '/^Release:/ s/'${RELEASE_OLD}'/'${RELEASE_NEW}'/' \
    -e "/^%changelog/ a\
* ${WEEKDAY} ${MONTH} ${DAY} ${YEAR} Yu Watanabe <watanabe.yu@gmail.com> - ${VERSION}-${RELEASE_NEW}.git${HASH_NEW_SHORT}\\
${CHANGE_LOG}" \
    -i ${SOURCE_DIR}/${REPO_NAME}.spec
if (( $? )); then
    echo "error: failed to update ${REPO_NAME}.spec" >&2
    exit 16
fi

git -C $SOURCE_DIR commit -a -m "$(echo -e ${COMMIT_LOG})"

#!/usr/bin/env bash

: #view unpushed commit of a checked-out branch ref. https://stackoverflow.com/a/2016954/248616
: #view unpushed branch of local repo ref. https://stackoverflow.com/a/15671218/248616

#params
FROM=$1
if [ -z "$FROM" ]; then
  FROM="$HOME/NN/code"
fi

#get all repo under $HOME/NN/code
REPOS=`find "$FROM" -name '.git' `

#check repo 1-by-1
UNPUSHED_BRANCHES=() #storing result for local branches that not pushed
UNPUSHED_COMMITS=()  #storing result for local commits that not pushed
function checkUnpushed() {
  REPO=$1
  s="$REPO/.." ; s=$(cd "$s" && pwd) ; REPO_FOLDER="$s"
  cd "$REPO_FOLDER" #go to repo folder

  #view unpushed branch of local repo ref. https://stackoverflow.com/a/15671218/248616
  localBranches=`git branch | sed s,..,,`
  for localBranch in ${localBranches}; do
    git config --get "branch.$localBranch.remote" | sed Q1 && \
      echo "$localBranch" && \
      UNPUSHED_BRANCHES+=("branch=$localBranch;repo=$REPO") #record found unpushed local branch
  done

  #view unpushed commit of local repo ref. https://stackoverflow.com/a/15671218/248616
  for localBranch in ${localBranches}; do
    git rev-parse --verify "$localBranch" > /dev/null ; errCode=$? #check if branch exists ref.https://stackoverflow.com/q/5167957/248616
    if [ "$errCode" -eq "0" ]; then #branh does exist
      commits=`git log origin/${localBranch}..${localBranch}` #view unpushed commit of local repo ref. https://stackoverflow.com/a/15671218/248616
      if [ ! -z "$commits" ]; then
        UNPUSHED_COMMITS+=("repo=$REPO_FOLDER;branch=$localBranch")
      fi
    fi
  done

  cd -- #return to where we were
}
for REPO in ${REPOS}; do
  echo "Checking $REPO"
  checkUnpushed "$REPO"
done

#output printing
echo && echo "Found local branches (${#UNPUSHED_BRANCHES[@]} found)" #array length ref. https://unix.stackexchange.com/a/193042/17671
for b in "${UNPUSHED_BRANCHES[@]}"; do
  echo "$b"
done

echo && echo "Found local commits (${#UNPUSHED_COMMITS[@]} found)" #array length ref. https://unix.stackexchange.com/a/193042/17671
for c in "${UNPUSHED_COMMITS[@]}"; do
  echo "$c"
done

#TODO also take care of uncommitted local changes

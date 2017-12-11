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
FOUND_LOCAL_BRANCHES='' #storing result for local branches that not pushed
function checkUnpushed() {
  REPO=$1
  cd "$REPO/.." #go to repo folder

  #view unpushed branch of local repo ref. https://stackoverflow.com/a/15671218/248616
  localBranches=`git branch | sed s,..,,`
  for localBranch in ${localBranches}; do
    git config --get "branch.$localBranch.remote" | sed Q1 && \
      echo "$localBranch" && \

      FOUND_LOCAL_BRANCHES="$FOUND_LOCAL_BRANCHES\n branch=$localBranch;repo=$REPO" #record found unpushed local branch
  done

  cd -- #return to where we were
}

for REPO in ${REPOS}; do
  echo "Checking $REPO"
  checkUnpushed "$REPO"
done

#output printing
FOUND_LOCAL_BRANCHES=`printf "$FOUND_LOCAL_BRANCHES"` #split string by new-line
echo && echo "Found local branches" #TODO how to print length of $FOUND_LOCAL_BRANCHES; this not working #echo && echo "Found local branches (${#FOUND_LOCAL_BRANCHES[@]} found)"
for f in ${FOUND_LOCAL_BRANCHES}; do
  echo "$f"
done

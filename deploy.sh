#!/bin/bash

set -o errexit -o nounset

# https://github.com/ofek/bit/blob/master/.travis/deploy_docs.sh
if [ "$TRAVIS_PYTHON_VERSION" != "3.4" ]
then
  echo "This is not the designated environment to publish docs. Skipping docs publishing."
  exit 0
fi

echo "Building docs..."

rev=$(git rev-parse --short HEAD)

cd sphinx/.build/html/

git init
git config user.name "Rodrigo Luger"
git config user.email "rodluger@gmail.com"

git remote add upstream "https://$GH_TOKEN@github.com/rodluger/everest3.git"
git fetch upstream && git reset upstream/gh-pages

# echo "example.com" > CNAME

touch .

git add -A .
git commit -m "rebuild pages at ${rev}"
git push -q upstream HEAD:gh-pages
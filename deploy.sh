#!/bin/bash
# Automatically update documentation on gh-pages branch with Travis. Based on
# http://www.steveklabnik.com/automatically_update_github_pages_with_travis_example/

# Exit on errors
set -o errexit -o nounset

# Prevent duplicate builds
# https://github.com/ofek/bit/blob/master/.travis/deploy_docs.sh
if [ "$TRAVIS_PYTHON_VERSION" != "3.4" ]
then
  echo "This is not the designated environment to publish docs. Skipping docs publishing."
  exit 0
fi

# Begin
echo "Building docs..."

# Get git hash
rev=$(git rev-parse --short HEAD)

# Create *new* git repo in html folder
cd sphinx/.build/html/
git init
git config user.name "Rodrigo Luger"
git config user.email "rodluger@gmail.com"

# We will push to gh-pages
git remote add upstream "https://$GH_TOKEN@github.com/rodluger/everest3.git"
git fetch upstream && git reset upstream/gh-pages

# Refresh all files
touch .

# Commit and push!
git add -A .
git commit -m "rebuild pages at ${rev}"
git push -q upstream HEAD:gh-pages
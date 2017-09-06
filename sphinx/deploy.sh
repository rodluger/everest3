#!/bin/bash
# Automatically update documentation on gh-pages branch with Travis. Based on
# http://www.steveklabnik.com/automatically_update_github_pages_with_travis_example/
# and
# https://github.com/dfm/imprs/blob/master/.travis.yml#L50

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

# Create orphan repo (DFM's hack)
cd $TRAVIS_BUILD_DIR
git checkout --orphan gh-pages

# Move html to dir above repo
mv sphinx/.build/html ../

# Delete everything in repo
git rm -rf .
rm -rf .

# Move html stuff back in and add it
mv ../html/* .
touch .nojekyll
git add -f .

# Commit and force push!
git -c user.name='travis' -c user.email='travis' commit -m "rebuild gh-pages at ${rev}"
git push -q -f https://$GH_TOKEN@github.com/$TRAVIS_REPO_SLUG gh-pages
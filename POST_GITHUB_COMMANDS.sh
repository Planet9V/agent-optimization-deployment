#!/bin/bash
# Commands to run AFTER GitHub repository is created
# These will be executed once remote is set up

echo "🔗 Post-GitHub Setup Commands"
echo "=============================="
echo ""

# Verify remote was added
if ! git remote get-url origin &> /dev/null; then
    echo "❌ Error: Remote 'origin' not configured"
    echo ""
    echo "Please add the remote first:"
    echo "  git remote add origin https://github.com/Planet9v/agent-optimization-deployment.git"
    exit 1
fi

echo "✅ Remote 'origin' configured:"
git remote -v
echo ""

# Show what will be pushed
echo "📦 Branches to push:"
echo ""
git branch -a
echo ""

echo "🚀 Ready to push! Run these commands:"
echo ""
echo "# Push deployment branch (main work)"
echo "git push -u origin deploy/agent-optimization"
echo ""
echo "# Push rollback safety branch"
echo "git push origin rollback/pre-deployment"
echo ""
echo "# Push master branch"
echo "git checkout master"
echo "git push -u origin master"
echo "git checkout deploy/agent-optimization"
echo ""

echo "After pushing, verify on GitHub:"
echo "  https://github.com/Planet9v/agent-optimization-deployment"
echo ""
echo "Then create a release tag:"
echo "  git tag -a v1.0.0 -m 'Release: Agent optimization implementations'"
echo "  git push origin v1.0.0"

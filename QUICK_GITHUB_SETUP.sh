#!/bin/bash
# Quick GitHub Setup Script for Planet9v/agent-optimization-deployment
# Generated: 2025-11-12

echo "🚀 Agent Optimization - GitHub Setup"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "Please cd to /home/jim/2_OXOT_Projects_Dev first"
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"
echo ""

# Option 1: Manual GitHub Web UI Setup
echo "Option 1: Manual Setup (RECOMMENDED)"
echo "====================================="
echo ""
echo "1. Go to: https://github.com/organizations/Planet9v/repositories/new"
echo "2. Repository name: agent-optimization-deployment"
echo "3. Visibility: Private"
echo "4. Description: Production deployment of agent optimization implementations (QW-001, QW-002, GAP-001) delivering 10-37x performance improvements"
echo "5. DO NOT initialize with README (we already have one)"
echo "6. Click 'Create repository'"
echo ""
echo "Then run these commands:"
echo ""
echo "  git remote add origin https://github.com/Planet9v/agent-optimization-deployment.git"
echo "  git push -u origin deploy/agent-optimization"
echo "  git push origin rollback/pre-deployment"
echo "  git push origin master"
echo ""
echo "---"
echo ""

# Option 2: GitHub CLI
echo "Option 2: GitHub CLI"
echo "===================="
echo ""
echo "If you have GitHub CLI installed and authenticated:"
echo ""
echo "  gh repo create Planet9v/agent-optimization-deployment \\"
echo "    --private \\"
echo "    --description 'Production deployment of agent optimization implementations (QW-001, QW-002, GAP-001) delivering 10-37x performance improvements' \\"
echo "    --source=. \\"
echo "    --remote=origin"
echo ""
echo "  git push -u origin deploy/agent-optimization"
echo "  git push origin rollback/pre-deployment"
echo "  git push origin master"
echo ""
echo "---"
echo ""

# Current status
echo "📊 Repository Status"
echo "===================="
echo ""
git log --oneline --all --graph -5
echo ""
echo "Files ready to push:"
git diff --stat master..deploy/agent-optimization
echo ""
echo "Total commits: $(git rev-list --count HEAD)"
echo "Current branch: $CURRENT_BRANCH"
echo "Uncommitted changes: $(git status --short | wc -l) files"
echo ""

echo "✅ Local deployment complete!"
echo "⏳ Waiting for GitHub repository setup..."
echo ""
echo "After setting up GitHub, verify with:"
echo "  git remote -v"
echo "  git branch -vv"

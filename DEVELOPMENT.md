# Development Workflow & Best Practices

**Project**: Agent Optimization Deployment
**Last Updated**: 2025-11-13
**MCP Integration**: ruv-swarm + claude-flow

---

## 🚨 Critical Backup Workflow

### Pre-Commit Backup Protocol

**MANDATORY**: Before ANY significant commit, backup critical systems:

1. **Neo4j Database** (4.2GB)
   ```bash
   # Export via Docker
   docker cp <neo4j-container>:/data backups/pre-commit-<timestamp>/neo4j/
   ```

2. **NER9 Model** (40K)
   ```bash
   # Backup NER agent and model files
   cp -r agents/ner_agent.py backups/pre-commit-<timestamp>/ner9/
   ```

3. **AgentDB State** (248K)
   ```bash
   # Backup implementation and tests
   cp -r lib/agentdb backups/pre-commit-<timestamp>/agentdb/
   cp -r tests/agentdb backups/pre-commit-<timestamp>/agentdb/tests/
   ```

4. **Documentation** (200K)
   ```bash
   # Backup all relevant documentation
   cp docs/GAP*.md backups/pre-commit-<timestamp>/docs/
   ```

### Backup Directory Structure
```
backups/
└── pre-commit-YYYY-MM-DD_HH-MM-SS/
    ├── neo4j/          # Database exports
    ├── ner9/           # NER model files
    ├── agentdb/        # AgentDB implementation
    └── docs/           # Critical documentation
```

---

## 📋 GitHub Workflow (Best Practices)

### 1. Pre-Commit Phase

**Always start with git status and branch check**:
```bash
git status
git branch
```

**Create backups BEFORE any changes**:
```bash
# Use automated backup script (see below)
./scripts/pre-commit-backup.sh
```

**Verify backup completion**:
```bash
du -sh backups/pre-commit-*/
ls -lah backups/pre-commit-*/
```

### 2. Feature Branch Creation

**NEVER work on main/master directly**:
```bash
# Create feature branch with descriptive name
git checkout -b feature/<gap-name>-<description>

# Examples:
git checkout -b feature/gap-002-agentdb-caching
git checkout -b feature/gap-003-query-control-system
git checkout -b bugfix/neo4j-connection-timeout
```

### 3. Staging Changes

**Stage only related changes**:
```bash
# Stage implementation files
git add lib/<module>/

# Stage tests
git add tests/<module>/

# Stage documentation
git add docs/<GAP>*.md

# Verify staged files
git status --short
```

### 4. Commit Message Format

**Use Conventional Commits**:
```bash
# Format: <type>(<scope>): <subject>
#
# Types: feat, fix, docs, style, refactor, test, chore
# Scope: module name (agentdb, query-control, etc.)
# Subject: concise description (imperative mood)

git commit -m "feat(agentdb): implement L1 cache with cosine similarity

## Summary
[Brief description of changes]

## Changes
- [List of key changes]

## Test Results
- [Test outcomes]

## Breaking Changes
[None or list]

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Use commit message files for complex commits**:
```bash
# Create detailed commit message
cat > .git-commit-message.txt << 'EOF'
feat(module): comprehensive description
...
EOF

# Commit using file
git commit -F .git-commit-message.txt
```

### 5. Pushing to Remote

**Push with upstream tracking**:
```bash
# First push sets upstream
git push -u origin feature/<branch-name>

# Subsequent pushes
git push
```

### 6. Pull Request Creation

**Use gh CLI for consistency**:
```bash
# Create PR with body file
gh pr create \
  --title "feat(module): Brief description" \
  --body-file .pr-description.md \
  --base main

# Or interactive mode
gh pr create --web
```

**PR Description Template** (see `.pr-description-gap002.md` for comprehensive example):
```markdown
# GAP-XXX: Feature Name

## 🎯 Overview
[Executive summary]

## 📊 Key Metrics
[Performance, test results, impact]

## 🔧 Technical Changes
[Detailed implementation changes]

## 📚 Documentation
[Documentation updates]

## ✅ Constitutional Compliance
[IRON LAW adherence]

## 🧪 Testing & Validation
[Test results and validation]

## 🚀 Deployment Readiness
[Production status and confidence]

## 📈 Impact Assessment
[System score and performance impact]

## 🔒 Security & Quality
[Security considerations]

## 📝 Lessons Learned
[What worked, what to improve]

## 🔄 Next Steps
[Follow-up actions]
```

---

## 🔧 Git Hooks for Automation

### Pre-Commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Pre-commit hook for automated backups

set -e

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="backups/pre-commit-$TIMESTAMP"

echo "🔒 Running pre-commit backup..."

# Create backup directories
mkdir -p "$BACKUP_DIR"/{neo4j,ner9,agentdb,docs}

# Backup Neo4j (if Docker container running)
if docker ps | grep -q neo4j; then
    echo "📦 Backing up Neo4j database..."
    docker cp $(docker ps | grep neo4j | awk '{print $1}'):/data "$BACKUP_DIR/neo4j/" 2>&1 | grep -v "permission denied" || true
fi

# Backup NER9
if [ -f "agents/ner_agent.py" ]; then
    echo "🧠 Backing up NER9 model..."
    cp -r agents/ner_agent.py "$BACKUP_DIR/ner9/"
fi

# Backup AgentDB
if [ -d "lib/agentdb" ]; then
    echo "🗄️  Backing up AgentDB..."
    cp -r lib/agentdb "$BACKUP_DIR/agentdb/"
    cp -r tests/agentdb "$BACKUP_DIR/agentdb/tests/" 2>/dev/null || true
fi

# Backup documentation
if ls docs/GAP*.md 1> /dev/null 2>&1; then
    echo "📚 Backing up documentation..."
    cp docs/GAP*.md "$BACKUP_DIR/docs/" 2>/dev/null || true
fi

echo "✅ Backup complete: $BACKUP_DIR"
echo "📊 Backup size: $(du -sh "$BACKUP_DIR" | awk '{print $1}')"

# Continue with commit
exit 0
```

**Install pre-commit hook**:
```bash
chmod +x .git/hooks/pre-commit
```

### Post-Merge Hook

Create `.git/hooks/post-merge`:
```bash
#!/bin/bash
# Post-merge hook for dependency updates

set -e

# Check for package.json changes
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q "package.json"; then
    echo "📦 package.json changed, running npm install..."
    npm install
fi

# Check for requirements.txt changes
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q "requirements.txt"; then
    echo "🐍 requirements.txt changed, updating Python dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Post-merge checks complete"
```

**Install post-merge hook**:
```bash
chmod +x .git/hooks/post-merge
```

---

## 🤖 MCP Integration in Git Workflow

### ruv-swarm Coordination

Use ruv-swarm for:
- **Performance analysis** during development
- **Bottleneck detection** before commits
- **Neural pattern learning** from successful workflows

```bash
# Initialize swarm for git operations
npx claude-flow@alpha mcp start
# Use mcp__ruv-swarm__swarm_init with mesh topology
# Use mcp__ruv-swarm__agent_spawn for coordinator agents
```

### claude-flow Orchestration

Use claude-flow for:
- **Code review** automation
- **Changelog generation**
- **Documentation validation**
- **Test execution** coordination

```bash
# Spawn claude-flow agents for PR workflow
# Use mcp__claude-flow__agent_spawn with reviewer type
# Use mcp__claude-flow__task_orchestrate for multi-step workflows
```

### Memory Coordination

Store workflow state across sessions:
```bash
# Store backup status
mcp__claude-flow__memory_usage action=store key=backup_status value=...

# Store PR creation status
mcp__claude-flow__memory_usage action=store key=pr_status value=...

# Retrieve for session resumption
mcp__claude-flow__memory_usage action=retrieve key=workflow_state
```

---

## 📊 Workflow Metrics

### Success Criteria

**Commit Quality**:
- ✅ All tests passing before commit
- ✅ Conventional commit message format
- ✅ Co-authored with Claude attribution
- ✅ Backups completed successfully

**PR Quality**:
- ✅ Comprehensive description with metrics
- ✅ All documentation updated
- ✅ Test results included
- ✅ Deployment readiness assessed

**Backup Quality**:
- ✅ All critical systems backed up
- ✅ Backup verification completed
- ✅ Total size documented
- ✅ Restoration tested periodically

### Timeline Standards

| Phase | Target | Actual (GAP-002) |
|-------|--------|------------------|
| Backup | <5 minutes | 3 minutes |
| Staging | <2 minutes | 1 minute |
| Commit | <1 minute | 30 seconds |
| Push | <1 minute | 30 seconds |
| PR Creation | <5 minutes | 3 minutes |
| **Total** | **<14 minutes** | **8 minutes** |

---

## 🔒 Security Best Practices

### Secrets Management

**NEVER commit secrets**:
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo "*.key" >> .gitignore
echo "credentials.json" >> .gitignore

# Verify no secrets in staged files
git diff --cached | grep -i "password\|secret\|key\|token" && exit 1 || true
```

### Pre-Commit Secret Scanning

Add to `.git/hooks/pre-commit`:
```bash
# Scan for common secret patterns
if git diff --cached | grep -iE "(password|secret|api[_-]?key|token|credentials)" > /dev/null; then
    echo "⚠️  WARNING: Potential secret detected in staged files!"
    echo "Review changes carefully before committing."
    read -p "Continue with commit? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

---

## 📝 Example: Complete Workflow

```bash
# 1. Check current state
git status
git branch

# 2. Create backups
./scripts/pre-commit-backup.sh

# 3. Create feature branch
git checkout -b feature/gap-003-query-control

# 4. Make changes (implement, test, document)
# ... development work ...

# 5. Stage changes
git add lib/query-control/
git add tests/query-control/
git add docs/GAP003*.md

# 6. Create commit message
cat > .git-commit-message.txt << 'EOF'
feat(query-control): implement pause/resume capability

## Summary
Implemented GAP-003 Query Control System with pause/resume,
model switching, and runtime command execution.

## Changes
- Added QueryControlManager with state machine
- Implemented pause(), resume(), terminate() operations
- Added model switching (Sonnet ↔ Haiku ↔ Opus)
- Created comprehensive test suite (8/8 passing)

## Test Results
✅ State transitions: PASS
✅ Pause/resume: PASS
✅ Model switching: PASS
✅ Command execution: PASS

## Breaking Changes
None. Backward compatible.

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF

# 7. Commit
git commit -F .git-commit-message.txt

# 8. Push
git push -u origin feature/gap-003-query-control

# 9. Create PR
cat > .pr-description.txt << 'EOF'
# GAP-003: Query Control System
...
EOF

gh pr create \
  --title "feat(query-control): GAP-003 Query Control System" \
  --body-file .pr-description.txt \
  --base main

# 10. Cleanup
rm .git-commit-message.txt .pr-description.txt
```

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Backup
./scripts/pre-commit-backup.sh

# Status
git status && git branch

# Feature branch
git checkout -b feature/<name>

# Stage & commit
git add <files>
git commit -F .commit-msg.txt

# Push & PR
git push -u origin <branch>
gh pr create --body-file .pr-desc.md

# Cleanup
git checkout main
git pull
git branch -d feature/<name>
```

### MCP Commands
```bash
# Initialize swarm
mcp__ruv-swarm__swarm_init topology=mesh

# Spawn agents
mcp__ruv-swarm__agent_spawn type=coordinator
mcp__claude-flow__agent_spawn type=reviewer

# Orchestrate task
mcp__ruv-swarm__task_orchestrate task="Create PR description"

# Store memory
mcp__claude-flow__memory_usage action=store key=workflow value=...
```

---

## 📚 Additional Resources

- **GAP-002 Example**: See commit `c83fd21` and PR #1
- **Backup Script**: `scripts/pre-commit-backup.sh`
- **Commit Template**: `.git-commit-message-gap002.txt`
- **PR Template**: `.pr-description-gap002.md`

---

**Status**: ✅ Production Workflow
**Last Validated**: 2025-11-13 (GAP-002)
**Success Rate**: 100% (GAP-002)
**Integration**: ruv-swarm + claude-flow

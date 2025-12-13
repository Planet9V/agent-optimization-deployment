# Kaggle API Authentication Setup

**Required for**: PROC-102 Kaggle Dataset Enrichment

## Setup Instructions

### 1. Get Kaggle API Credentials

1. Go to https://www.kaggle.com/settings/account
2. Scroll to "API" section
3. Click "Create New Token"
4. Download `kaggle.json` file

### 2. Install Credentials

```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 3. Verify Setup

```bash
kaggle datasets list --max-size 1
```

## Expected kaggle.json Format

```json
{
  "username": "your_kaggle_username",
  "key": "your_api_key_here"
}
```

## PROC-102 Ready to Execute

Once credentials are installed, run:

```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
./scripts/proc_102_kaggle_enrichment.sh
```

This will:
1. Download CVE & CWE dataset (215,780 CVEs)
2. Enrich 316,552 existing CVE nodes with CVSS v2/v3/v4 scores
3. Create IS_WEAKNESS_TYPE relationships to CWE nodes
4. Store results in claude-flow memory

**Estimated Duration**: 60-120 minutes

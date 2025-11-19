# NVD CVE Import Script - Quick Start

## 🚀 Quick Start (3 Steps)

### 1. Pre-flight Check
```bash
./scripts/verify_nvd_import_ready.sh
```

### 2. Run Import
```bash
./import_nvd_2018_2019.py
```

### 3. Monitor Progress
```bash
tail -f nvd_import_2018_2019.log
```

## 📊 What Gets Imported

- **CVE Count**: ~35,000-40,000 (2018-2019)
- **Properties**: CVE ID, CVSS score, severity, description, dates
- **Relationships**: CVE → CWE (weakness)
- **Time**: 2-5 minutes

## 📁 Files

- `import_nvd_2018_2019.py` - Main import script
- `docs/NVD_IMPORT_GUIDE.md` - Complete documentation
- `docs/NVD_IMPORT_SUMMARY.md` - Technical summary
- `scripts/verify_nvd_import_ready.sh` - Pre-flight check

## 🔍 Verify Import

```cypher
// Count imported CVEs
MATCH (c:CVE)
WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
RETURN count(c) as total

// Check severity distribution
MATCH (c:CVE)
WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
RETURN c.severity, count(*) as count
ORDER BY count DESC

// Top CWEs
MATCH (c:CVE)-[:EXPLOITS_WEAKNESS]->(w:CWE)
WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
RETURN w.cwe_id, count(c) as cve_count
ORDER BY cve_count DESC
LIMIT 20
```

## 📖 Full Documentation

See `docs/NVD_IMPORT_GUIDE.md` for:
- Detailed usage instructions
- Troubleshooting guide
- Performance optimization
- API reference
- Advanced queries

## ⚡ Background Execution

```bash
# Run in background
nohup python3 import_nvd_2018_2019.py > nvd_import.out 2>&1 &

# Monitor
tail -f nvd_import_2018_2019.log

# Check progress
cat .nvd_import_progress.json
```

## ✅ Success Indicators

Expected output:
```
============================================================
IMPORT SUMMARY
============================================================
CVEs Processed: 37,824
CVEs Created: 37,824
CWEs Linked: 45,312
Errors: 0
Duration: 0:04:32
============================================================
```

## 🆘 Troubleshooting

**Script won't start?**
- Run: `./scripts/verify_nvd_import_ready.sh`

**Import too slow?**
- Normal: Rate limited to 5 requests per 30 seconds
- Get API key from NVD for faster imports

**Low CVE count?**
- Check: `cat .nvd_import_progress.json`
- Review: `tail -50 nvd_import_2018_2019.log`

---

**Ready to import? Run: `./import_nvd_2018_2019.py`**

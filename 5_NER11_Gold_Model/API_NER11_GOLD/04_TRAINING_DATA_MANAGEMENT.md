# Training Data Management Guide

## Overview
This guide explains how to access the local training data within the container and how to update it for future model versions (e.g., NER12 Gold).

## 1. Accessing Training Data

The training data is located at `/app/training_data` inside the container.

### Direct Access via Shell
```bash
docker exec -it ner11-api bash
cd /app/training_data
ls -F
```

You will see:
- `custom_data/`: Your proprietary gold standard data (3.0x weight)
- `external_data/`: Public datasets (1.0x weight)
- `final_training_set/`: The processed `.spacy` files used for training
- `TRAINING_DATA_MANIFEST.md`: Audit trail of all data

## 2. Updating Data for NER12

To train the next version (NER12), follow these steps:

### Step A: Add New Data
1.  Place new text files in `training_data/custom_data/`.
2.  Ensure they follow the entity annotation format.

### Step B: Mount Local Data
When running the container, mount your local `training_data` folder to persist changes:

```bash
docker run -d \
  -v $(pwd)/training_data:/app/training_data \
  -p 8000:8000 \
  ner11-gold-api
```

### Step C: Retrain
Use the provided training script inside the container:

```bash
docker exec -it ner11-api bash
./start_training.sh
```

This will:
1.  Convert new data to `.spacy` format.
2.  Combine it with existing data.
3.  Train a new model (output to `models/ner12_v1`).

## 3. Data Backup

Always backup your `training_data` folder before major updates:

```bash
tar -czf training_data_backup_$(date +%Y%m%d).tar.gz training_data/
```

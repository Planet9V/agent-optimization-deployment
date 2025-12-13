import os
import shutil

# Config
TARGET_DIR = "/Users/jim/MMM_Pyschometric_Therapy/06_mckenney_lacan_unified_theory"
BACKUP_DIR = os.path.join(TARGET_DIR, "_legacy_backup")

# The V9.8 "Keep List" (The Standardized Corpus)
KEEP_LIST = {
    "00_Unified_Theory_Master_Index.md",
    "01_Vol_00_Laymans_Primer.md",
    "02_Vol_01_Foundations.md",
    "03_Vol_02_Kinematics.md",
    "04_Vol_03_Dynamics.md",
    "05_Vol_04_Network_Physics.md",
    "06_Vol_05_Thermodynamics.md",
    "07_Vol_06_Technical_Architecture.md",
    "08_Vol_07_Predictive_Mechanics.md",
    "09_Vol_08_Psychohistory_Engine.md",
    "10_Vol_09_Reference_Bibliography.md",
    "11_Vol_10_Appendix_Math_Codex.md",
    "12_Vol_11_Computational_Sim.md",
    "13_Vol_12_Digital_Twin.md",
    "14_Vol_13_Organizational_Physics.md",
    "15_Vol_14_Advanced_Simulations.md",
    "16_Vol_15_Cognitive_Bias_Atlas.md",
    "90_Archive_Deep_Layering_Plan.md",
    "91_Archive_Master_Syllabus.md",
    "92_Archive_MoE_Review.md",
    "93_Archive_Math_Plan.md",
    "94_Archive_Critique_Grand_Eq.md",
    "final_cleanup.py"
}

def clean_directory():
    # Ensure backup dir exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")

    # Scan and Move
    moved_count = 0
    for filename in os.listdir(TARGET_DIR):
        file_path = os.path.join(TARGET_DIR, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
            
        # Move if not in Keep List
        if filename not in KEEP_LIST:
            dest_path = os.path.join(BACKUP_DIR, filename)
            try:
                shutil.move(file_path, dest_path)
                print(f"Moved: {filename} -> _legacy_backup/")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")

    print(f"\nCleanup Complete. {moved_count} legacy files moved to backup.")
    print(f"Remaining clean files: {len(os.listdir(TARGET_DIR)) - 1}") # -1 for the backup dir

if __name__ == "__main__":
    clean_directory()

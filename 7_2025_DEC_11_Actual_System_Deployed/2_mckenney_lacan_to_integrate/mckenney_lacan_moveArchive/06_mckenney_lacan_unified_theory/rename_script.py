import os

base_dir = "/Users/jim/MMM_Pyschometric_Therapy/06_mckenney_lacan_unified_theory"

mapping = {
    # Main Sequence
    "02_Vol_II_Kinematics.md": "03_Vol_02_Kinematics.md",
    "03_Vol_III_Dynamics.md": "04_Vol_03_Dynamics.md",
    "04_Vol_IV_Directors_Score.md": "05_Vol_04_Network_Physics.md",
    "05_Vol_V_Synthesis.md": "06_Vol_05_Thermodynamics.md",
    "06_Vol_VI_Technical_Architecture.md": "07_Vol_06_Technical_Architecture.md",
    "07_Vol_VII_Bayesian_Prediction.md": "08_Vol_07_Predictive_Mechanics.md",
    "08_Vol_VIII_Psychohistory_Engine.md": "09_Vol_08_Psychohistory_Engine.md",
    "09_Bibliography.md": "10_Vol_09_Reference_Bibliography.md",
    "10_Appendix_A_Math_Codex.md": "11_Vol_10_Appendix_Math_Codex.md",
    "12_Vol_XII_Computational_Simulation.md": "13_Vol_12_Computational_Sim.md",
    "13_Vol_XIII_Digital_Twin.md": "14_Vol_13_Digital_Twin.md",
    "14_Vol_XIV_Organizational_Physics.md": "15_Vol_14_Organizational_Physics.md",
    "16_Vol_XV_Advanced_Simulations.md": "16_Vol_15_Advanced_Simulations.md",
    "17_Vol_XVI_Cognitive_Bias_Atlas.md": "17_Vol_16_Cognitive_Bias_Atlas.md",
    # Archives
    "00_Deep_Layering_Plan.md": "90_Archive_Deep_Layering_Plan.md",
    "00_Unified_Theory_Master_Syllabus.md": "91_Archive_Master_Syllabus.md",
    "08_MoE_Critical_Review.md": "92_Archive_MoE_Review.md",
    "11_Math_Integration_Plan_v9.2.md": "93_Archive_Math_Plan.md",
    "15_Critique_Grand_Equation.md": "94_Archive_Critique_Grand_Eq.md"
}

for src, dst in mapping.items():
    src_path = os.path.join(base_dir, src)
    dst_path = os.path.join(base_dir, dst)
    if os.path.exists(src_path):
        try:
            os.rename(src_path, dst_path)
            print(f"RENAMED: {src} -> {dst}")
        except Exception as e:
            print(f"ERROR: Could not rename {src} to {dst}: {e}")
    elif os.path.exists(dst_path):
        print(f"SKIPPED: {dst} already exists")
    else:
        print(f"MISSING: {src} not found")

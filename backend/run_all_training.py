import subprocess
import sys
import os

def run_script(script_path):
    print(f"\n🚀 Running {script_path} ...")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path}:")
        print(e)
    else:
        print("✅ Done.")

if __name__ == "__main__":
    print("🧠 Starting full model training pipeline...")

    base_path = os.path.join("app", "train")
    scripts = [
        "clean_feature_hybrid.py",
        "train_content.py",
        "train_collaborative.py"
    ]

    for script in scripts:
        run_script(os.path.join(base_path, script))

    print("\n🏁 Training pipeline completed.")

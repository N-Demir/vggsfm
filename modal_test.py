import modal
import subprocess
import os
import argparse

app = modal.App("vggsfm-training")
image = modal.Image.from_gcp_artifact_registry(
    "gcr.io/tour-project-442218/vggsfm",
    secret=modal.Secret.from_name(
        "gcp-credentials",
        required_keys=["SERVICE_ACCOUNT_JSON"],
    ),
)

@app.function(gpu="T4", image=image, secrets=[modal.Secret.from_name("gcp-credentials")])
def train_vggsfm(dataset: str | None = None):
    if dataset is None:
        print("No dataset specified. Please provide a dataset name.")
        return
        
    print(f"Starting VGGSfM training on remote worker for dataset: {dataset}!")
    
    # Make the shell script executable
    os.chmod("run_training.sh", 0o755)
    
    try:
        # Run the shell script with dataset argument
        subprocess.run(["./run_training.sh", dataset], check=True)
        print("Training completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Training failed with error: {e}")
        raise

@app.local_entrypoint()
def main():
    parser = argparse.ArgumentParser(description='Run VGGSfM training on Modal')
    parser.add_argument('--dataset', type=str, help='Name of the dataset to train on (e.g., tandt/truck)')
    args = parser.parse_args()
    
    train_vggsfm.remote(args.dataset)

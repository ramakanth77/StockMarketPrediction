import os
import subprocess

def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_name}: {e}")

if __name__ == "__main__":
    scripts = [
        'data_collection.py',
        'data_preprocessing.py',
        'eda.py',
        'model_implementation.py',
        'model_deployment.py'
    ]

    for script in scripts:
        run_script(script)

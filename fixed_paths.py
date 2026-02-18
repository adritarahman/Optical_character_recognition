import os
import yaml


local_mlruns_path = r"C:\Users\Testing\OneDrive\Desktop\OCR\mlruns"

def fix_mlflow_paths(root_dir):
    
    new_base_uri = f"file:///{root_dir.replace(os.sep, '/')}"
    
    print(f"Updating meta.yaml files to point to: {new_base_uri}")
    
    count = 0
    for root, dirs, files in os.walk(root_dir):
        if 'meta.yaml' in files:
            yaml_path = os.path.join(root, 'meta.yaml')
            
            with open(yaml_path, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue
            
            if not data: continue
            
            changed = False
            for key in ['artifact_location', 'artifact_uri']:
                if key in data and data[key] is not None:
                    
                    if 'mlruns' in data[key]:
                        parts = data[key].split('mlruns')
                        suffix = parts[-1]
                        data[key] = new_base_uri + suffix
                        changed = True
            
            if changed:
                with open(yaml_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)
                count += 1

    print(f"✅ Successfully updated {count} meta.yaml files.")

if __name__ == "__main__":
    fix_mlflow_paths(local_mlruns_path)
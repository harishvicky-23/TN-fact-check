import os
import yaml

tasks_yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks.yaml')
with open(tasks_yaml_path, 'r', encoding='utf-8') as f:
    tasks_config = yaml.safe_load(f)

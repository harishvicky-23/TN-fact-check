import os
import yaml

agents_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agents.yaml')
with open(agents_config_path, 'r', encoding='utf-8') as f:
    agents_config = yaml.safe_load(f)

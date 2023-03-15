import yaml
from rich import print as rprint
from pprint import pprint

with open("R1.yaml") as file:
    config_file = yaml.safe_load(file)
    pprint(config_file)
   

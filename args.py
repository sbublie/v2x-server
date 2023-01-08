import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', required=False, default='live', choices=['live', 'debug'])
args = parser.parse_args()

"""Compatibility entry point; pass --run-id and optional sampler settings."""
import sys
from bayesian_workflow import main

if __name__ == "__main__":
    for model in ['missing']:
        main(["--model", model, *sys.argv[1:]])

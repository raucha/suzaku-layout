#!/bin/bash
cd "$(dirname "$0")"

pipenv run python -m unittest discover tests
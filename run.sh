#!/bin/bash

script_home=$(dirname "$(realpath "$0")")

cd $script_home

source .venv/bin/activate

python etl_imdb.py 
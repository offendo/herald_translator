#!/bin/bash
mkdir -p data/results
python -m run_translate_verify data/$1 data/results/$1
python -m run_backtrans_nli data/results/$1
#!/bin/sh

cd /home/jmlee
source /home/jmlee/.bashrc
conda activate e2e-negotiation
cd /home/jmlee/workspace/e2e-negotiation-mcts/src
python selfplay.py --condor_node_idx=$1

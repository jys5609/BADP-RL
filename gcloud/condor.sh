#!/bin/sh

cd /home/starjongmin
source /home/starjongmin/.bashrc
conda activate bamcp-negotiation
cd /home/starjongmin/bucket/BAMCP_negotiation/src
python selfplay.py --condor_node_idx=$1

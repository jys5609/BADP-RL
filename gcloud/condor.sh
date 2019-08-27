#!/bin/sh

cd /mnt/nfs/BAMCP_negotiation/src
/home/starjongmin/miniconda/envs/bamcp-negotiation/bin/python selfplay.py --condor_node_idx=$1 --condor_num_nodes=100

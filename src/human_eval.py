# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import pdb
import re
import random

import numpy as np
import torch
from torch import optim
from torch import autograd
import torch.nn as nn

from agent import *
import utils
from utils import ContextGenerator, CondorContextGenerator
from human_dialog import Dialog, DialogLogger
from models.rnn_model import RnnModel
from models.latent_clustering_model import LatentClusteringPredictionModel, BaselineClusteringModel
import domain
import os

class SelfPlay(object):
    def __init__(self, dialog, ctx_gen, args, logger=None):
        self.dialog = dialog
        self.ctx_gen = ctx_gen
        self.args = args
        self.logger = logger if logger else DialogLogger()

    def run(self):
        if len(self.args.selfplay_data_path) > 0:
            if not os.path.exists(self.args.selfplay_data_path):
                os.makedirs(self.args.selfplay_data_path)
            data_saver = open(self.args.selfplay_data_path + '/data.txt.tmp', 'w')

        n = 0
        for ctxs in self.ctx_gen.iter(nepoch=3):
            n += 1
            # self.logger.dump('* Dialogue %d' % n)
            ##
            self.logger.dump('=' * 80)
            self.dialog.run(ctxs, self.logger, 5000, data_saver)
            self.logger.dump('=' * 80)
            self.logger.dump('')
            if n % 1 == 0:
                self.logger.dump('%d: %s' % (n, self.dialog.show_metrics()), forced=True)
            break

        if len(self.args.selfplay_data_path) > 0:
            data_saver.close()


def get_agent_type(model, smart=False):
    if isinstance(model, LatentClusteringPredictionModel):
        if smart:
            return LatentClusteringRolloutAgent
        else:
            return LatentClusteringAgent
    elif isinstance(model, RnnModel):
        if smart:
            return RnnRolloutAgent
        else:
            return RnnAgent
    elif isinstance(model, BaselineClusteringModel):
        if smart:
            return BaselineClusteringRolloutAgent
        else:
            return BaselineClusteringAgent
    else:
        assert False, 'unknown model type: %s' % (model)

def selfplay_data_splitter(selfplay_data_path):
    with open(selfplay_data_path + '/data.txt', 'r') as file:
        data = file.read().strip()
        data = data.split('\n')
    np.random.shuffle(data)
    N = len(data)
    train_N = int(N * 0.9)
    train_data = data[:train_N]
    valid_data = data[train_N:]
    test_data = data[train_N:]
    with open(selfplay_data_path + '/train.txt', 'w') as file:
        file.write('\n'.join(train_data) + '\n')
    with open(selfplay_data_path + '/val.txt', 'w') as file:
        file.write('\n'.join(valid_data) + '\n')
    with open(selfplay_data_path + '/test.txt', 'w') as file:
        file.write('\n'.join(test_data) + '\n')

def main():
    parser = argparse.ArgumentParser(description='selfplaying script')
    parser.add_argument('--alice_model_file', type=str,
        help='Alice model file')
    parser.add_argument('--alice_forward_model_file', type=str,
        help='Alice forward model file')
    parser.add_argument('--bob_model_file', type=str,
        help='Bob model file')
    parser.add_argument('--context_file', type=str,
        help='context file')
    parser.add_argument('--temperature', type=float, default=1.0,
        help='temperature')
    parser.add_argument('--pred_temperature', type=float, default=1.0,
        help='temperature')
    parser.add_argument('--verbose', action='store_true', default=False,
        help='print out converations')
    parser.add_argument('--seed', type=int, default=1,
        help='random seed')
    parser.add_argument('--score_threshold', type=int, default=6,
        help='successful dialog should have more than score_threshold in score')
    parser.add_argument('--max_turns', type=int, default=20,
        help='maximum number of turns in a dialog')
    parser.add_argument('--log_file', type=str, default='',
        help='log successful dialogs to file for training')
    parser.add_argument('--smart_alice', action='store_true', default=False,
        help='make Alice smart again')
    parser.add_argument('--diverse_alice', action='store_true', default=False,
        help='make Alice smart again')
    parser.add_argument('--rollout_bsz', type=int, default=3,
        help='rollout batch size')
    parser.add_argument('--rollout_count_threshold', type=int, default=3,
        help='rollout count threshold')
    parser.add_argument('--smart_bob', action='store_true', default=False,
        help='make Bob smart again')
    parser.add_argument('--selection_model_file', type=str,  default='',
        help='path to save the final model')
    parser.add_argument('--rollout_model_file', type=str,  default='',
        help='path to save the final model')
    parser.add_argument('--diverse_bob', action='store_true', default=False,
        help='make Alice smart again')
    parser.add_argument('--ref_text', type=str,
        help='file with the reference text')
    parser.add_argument('--cuda', action='store_true', default=False,
        help='use CUDA')
    parser.add_argument('--domain', type=str, default='object_division',
        help='domain for the dialogue')
    parser.add_argument('--visual', action='store_true', default=False,
        help='plot graphs')
    parser.add_argument('--eps', type=float, default=0.0,
        help='eps greedy')
    parser.add_argument('--data', type=str, default='data/negotiate',
        help='location of the data corpus')
    parser.add_argument('--unk_threshold', type=int, default=20,
        help='minimum word frequency to be in dictionary')
    parser.add_argument('--bsz', type=int, default=16,
        help='batch size')
    parser.add_argument('--validate', action='store_true', default=False,
        help='plot graphs')
    parser.add_argument('--sampling', type=str, default='posterior', help='sampling method')
    parser.add_argument('--search_type', type=str, default='mcts', help='search method')

    parser.add_argument('--selfplay_data_path', type=str, default='data/negotiate_selfplay', help='selfplay data path')
    parser.add_argument('--condor_num_nodes', type=int, default=1, help='condor num nodes')
    parser.add_argument('--condor_node_idx', type=int, default=0, help='condor node index (0 <= idx < num_nodes)')

    args = parser.parse_args()
    ## parameter setup

    args.cuda = False
    args.context_file = 'data/human_eval/selfplay.txt'
    args.selection_model_file = 'selection_model.th'
    args.verbose = True
    args.log_file = 'selfplay_log.txt'

    utils.use_cuda(args.cuda)
    utils.set_seed(args.seed)

    alice_model = utils.load_model(args.alice_model_file)
    alice_ty = get_agent_type(alice_model, args.smart_alice)
    alice = alice_ty(alice_model, args, name='Alice', train=False)
    alice.vis = args.visual

    name = input("Type your name: ")
    num_exp = input("How many times: ")

    print()
    print("========Dialogue Example 1========")
    print("A: hi i would like the book and ball and you can have the hats <eos>\n"
          "B: i can give you either the book or the ball <eos>\n"
          "A: ill take the book <eos>\n"
          "B: ok i will take the hats and ball <eos>\n"
          "A: deal <eos>\n"
          "B: <selection>\n")

    print("========Dialogue Example 2========")
    print("A: hi , i would like the ball and 2 hats and you can have the book and 1 hat <eos>\n"
          "B: i rather like the ball also . you can have all three hats if i get the ball and book . <eos>\n"
          "A: ok , i can do that . <eos>\n"
          "B: <selection>\n")

    print("========Dialogue Example 3========")
    print("A: i want the ball <eos>\n"
          "B: ok , i get rest <eos>\n"
          "A: deal <eos>\n"
          "B: <selection>\n")

    print("START!!!!!!!!\n")

    human = HumanAgent(domain.get_domain(args.domain), name)
    ctx_gen = ContextGenerator(args.context_file)

    model_names = ['LIKELIHOOD', 'REINFORCE', 'BADP-RL', 'H-REINFORCE', 'FULL-MODEL']
    model_idxs = {'LIKELIHOOD':0, 'REINFORCE':1, 'BADP-RL':2, 'H-REINFORCE':3, 'FULL-MODEL':4}
    model_files = ['likelihood.th', 'reinforce.th', 'badp_rl.th', 'h_reinforce.th', 'full_model.th']

    random.shuffle(model_names)
    model_names *= num_exp

    for model_name in model_names:
        args.alice_model_file = model_files[model_idxs[model_name]]
        alice_model = utils.load_model(args.alice_model_file)
        alice_ty = get_agent_type(alice_model, args.smart_alice)
        alice = alice_ty(alice_model, args, name=model_name, train=False)
        alice.vis = args.visual

        dialog = Dialog([alice, human], args)
        logger = DialogLogger(verbose=args.verbose, log_file=args.log_file + '.tmp')

        selfplay = SelfPlay(dialog, ctx_gen, args, logger)
        selfplay.run()


if __name__ == '__main__':
    main()

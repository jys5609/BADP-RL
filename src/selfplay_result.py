import numpy as np
import re

for selfplay_round in range(5):
    num_condor_nodes = 25

    total_N = 0
    total_agree = 0
    total_dialog_len = 0
    total_mcts_rew = 0
    total_agree_mcts_rew = 0
    total_bob_rew = 0
    total_agree_bob_rew = 0
    for idx in range(num_condor_nodes):
        with open('selfplay_log_%d_%02d.txt' % (selfplay_round, idx), 'r') as file:
            lines = file.read().strip().split('\n')
            summary = lines[-1]
            m = re.search('(\d+): dialog_len=(.*) sent_len=(.*) agree=(.*)% moving_agree=(.*)% advantage=(.*) moving_advantage=(.*) time=(.*)s ' +
                          'comb_rew=(.*) agree_comb_rew=(.*) mcts_rew=(.*) mcts_moving_rew=(.*) agree_mcts_rew=(.*) mcts_sel=(.*)% mcts_unique=(.*) bob_rew=(.*) ' +
                          'bob_moving_rew=(.*) agree_bob_rew=(.*) bob_sel=(.*)% bob_unique=(.*)', summary)
            N = int(m.group(1))
            dialog_len = float(m.group(2))
            sent_len = float(m.group(3))
            agree = float(m.group(4))
            moving_agree = float(m.group(5))
            advantage = float(m.group(6))
            moving_advantage = float(m.group(7))
            time = float(m.group(8))
            comb_rew = float(m.group(9))
            agree_comb_rew = float(m.group(10))
            mcts_rew = float(m.group(11))
            mcts_moving_rew = float(m.group(12))
            agree_mcts_rew = float(m.group(13))
            mcts_sel = float(m.group(14))
            mcts_unique = float(m.group(15))
            bob_rew = float(m.group(16))
            bob_moving_rew = float(m.group(17))
            agree_bob_rew = float(m.group(18))
            bob_sel = float(m.group(19))
            bob_unique = float(m.group(20))

            total_N += N
            total_agree += N * agree
            total_dialog_len += N * dialog_len
            total_mcts_rew += N * mcts_rew
            total_agree_mcts_rew += N * agree_mcts_rew
            total_bob_rew += N * bob_rew
            total_agree_bob_rew += N * agree_bob_rew
            # print('N=%d / dialog_len=%f / mcts_rew=%f / agree_mcts_rew=%f / bob_rew=%f / agree_bob_rew=%f' % (N, dialog_len, mcts_rew, agree_mcts_rew, bob_rew, agree_bob_rew))

    print('============ Selfplay round %d =================' % selfplay_round)
    print('N=%d / agree=%f / dialog_len=%f / mcts_rew=%f / agree_mcts_rew=%f / bob_rew=%f / agree_bob_rew=%f' %
          (total_N, total_agree / total_N, total_dialog_len / total_N, total_mcts_rew / total_N, total_agree_mcts_rew / total_N, total_bob_rew / total_N, total_agree_bob_rew / total_N))

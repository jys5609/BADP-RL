import shutil
import os

selfplay_round = 5
num_condor_nodes = 25

# selfplay data
train_data = []
val_data = []
test_data = []

for idx in range(num_condor_nodes):
    dirname = 'data/negotiate_selfplay_%d_%02d' % (selfplay_round, idx)
    with open('%s/train.txt' % dirname, 'r') as file:
        train_data += file.read().strip().split('\n')
    with open('%s/val.txt' % dirname, 'r') as file:
        val_data += file.read().strip().split('\n')
    with open('%s/test.txt' % dirname, 'r') as file:
        test_data += file.read().strip().split('\n')

save_dirname = 'data/negotiate_selfplay_%d' % selfplay_round
if not os.path.exists(save_dirname):
    os.makedirs(save_dirname)

with open('%s/train.txt' % save_dirname, 'w') as file:
    file.write('\n'.join(train_data) + '\n')
with open('%s/val.txt' % save_dirname, 'w') as file:
    file.write('\n'.join(val_data) + '\n')
with open('%s/test.txt' % save_dirname, 'w') as file:
    file.write('\n'.join(test_data) + '\n')

# after aggregation... delete splitted directories
for idx in range(num_condor_nodes):
    dirname = 'data/negotiate_selfplay_%d_%02d' % (selfplay_round, idx)
    try:
        shutil.rmtree(dirname)
    except OSError as e:
        if e.errno == 2:
            print('No such file or directory to remove')
            pass
        else:
            raise

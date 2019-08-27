import shutil
import os

selfplay_round = 1
num_condor_nodes = 100
sampling = 'posterior'

# selfplay data
train_data = []
val_data = []
test_data = []

for idx in range(num_condor_nodes):
    dirname = 'data/negotiate_selfplay_%s_%d_%02d' % (sampling, selfplay_round, idx)
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

# Aggregate log files...
log_text = ""
for idx in range(num_condor_nodes):
    filename = 'selfplay_log_%s_%d_%02d.txt' % (sampling, selfplay_round, idx)
    with open(filename) as file:
        log_text += file.read()

with open('selfplay_log_%s_%d.txt' % (sampling, selfplay_round)) as file:
    file.write(log_text)

# After aggregation, delete each of separated log files...
for idx in range(num_condor_nodes):
    filename = 'selfplay_log_%s_%d_%02d.txt' % (sampling, selfplay_round, idx)
    try:
        os.remove(filename)
    except:
        print('No such file to remove?')


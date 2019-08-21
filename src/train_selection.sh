python train.py \
  --data data/negotiate_selfplay_1 \
  --cuda \
  --bsz 16 \
  --clip 2.0 \
  --decay_every 1 \
  --decay_rate 5.0 \
  --domain object_division \
  --dropout 0.1 \
  --init_range 0.2 \
  --lr 0.001 \
  --max_epoch 7 \
  --min_lr 1e-05 \
  --model_type selection_model \
  --momentum 0.1 \
  --nembed_ctx 128 \
  --nembed_word 128 \
  --nhid_attn 128 \
  --nhid_ctx 64 \
  --nhid_lang 128 \
  --nhid_sel 128 \
  --nhid_strat 256 \
  --unk_threshold 20 \
  --skip_values \
  --sep_sel \
  --model_file selection_model_1.th

#--data data/negotiate --cuda --bsz 16 --clip 2.0 --decay_every 1 --decay_rate 5.0 --domain object_division --dropout 0.1 --init_range 0.2 --lr 0.001 --max_epoch 10 --min_lr 1e-05 --model_type selection_model --momentum 0.1 --nembed_ctx 128 --nembed_word 128 --nhid_attn 128 --nhid_ctx 64 --nhid_lang 128 --nhid_sel 128 --nhid_strat 256 --unk_threshold 20 --skip_values --sep_sel --model_file selection_model_1.th
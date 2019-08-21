# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import torch
from torch.nn import functional
from torch.autograd import Variable

from engines import EngineBase, Criterion


def _sequence_mask(sequence_length, max_len=None):
    if max_len is None:
        max_len = sequence_length.data.max()
    batch_size = sequence_length.size(0)
    seq_range = torch.range(0, max_len - 1).long()
    seq_range_expand = seq_range.unsqueeze(0).expand(batch_size, max_len)
    seq_range_expand = Variable(seq_range_expand)
    if sequence_length.is_cuda:
        seq_range_expand = seq_range_expand.cuda()
    seq_length_expand = (sequence_length.unsqueeze(1).expand_as(seq_range_expand))
    return seq_range_expand < seq_length_expand


def compute_loss(logits_flat, target, mask):
    """
    Args:
        logits: A Variable containing a FloatTensor of size
            (batch, max_len, num_classes) which contains the
            unnormalized probability for each class.
        target: A Variable containing a LongTensor of size
            (batch, max_len) which contains the index of the true
            class for each corresponding step.
        length: A Variable containing a LongTensor of size (batch,)
            which contains the length of each data in a batch.
    Returns:
        loss: An average loss value masked by the length.
    """

    # logits_flat: (batch * max_len, num_classes)
    # logits_flat = logits.view(-1, logits.size(-1))
    # log_probs_flat: (batch * max_len, num_classes)
    log_probs_flat = functional.log_softmax(logits_flat, 1)
    # target_flat: (batch * max_len, 1)
    target_flat = target.view(-1, 1)
    # losses_flat: (batch * max_len, 1)
    losses_flat = -torch.gather(log_probs_flat, dim=1, index=target_flat)
    # losses: (batch, max_len)
    losses = losses_flat.view(*target.size())
    # mask: (batch, max_len)
    # mask = _sequence_mask(sequence_length=length, max_len=target.size(1))
    losses = losses * mask.float()
    loss = losses.sum() / float(mask.nonzero().size(0))
    return loss


class RnnEngine(EngineBase):
    def __init__(self, model, args, verbose=False):
        super(RnnEngine, self).__init__(model, args, verbose)

    def _forward(model, batch):
        ctx, inpt, tgt, sel_tgt, mask = batch
        ctx = Variable(ctx)
        inpt = Variable(inpt)
        tgt = Variable(tgt)
        sel_tgt = Variable(sel_tgt)

        out, sel_out = model(inpt, ctx)
        return out, tgt, sel_out, sel_tgt, mask

    def train_batch(self, batch):
        out, tgt, sel_out, sel_tgt, mask = RnnEngine._forward(self.model, batch)
        # loss = self.crit(out, tgt)
        loss = compute_loss(out, tgt, mask)
        loss += self.sel_crit(sel_out, sel_tgt) * self.model.args.sel_weight
        self.opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.args.clip)
        self.opt.step()
        return loss.item()

    def valid_batch(self, batch):
        with torch.no_grad():
            out, tgt, sel_out, sel_tgt, mask = RnnEngine._forward(self.model, batch)
        valid_loss = mask.nonzero().size(0) * compute_loss(out, tgt, mask)
        select_loss = self.sel_crit(sel_out, sel_tgt)
        return valid_loss.item(), select_loss.item(), 0

# Bayes-Adaptive Monte-Carlo Planning and Learning for Goal-Oriented Dialogues

This repository is the implementation of ["Bayes-Adaptive Monte-Carlo Planning and Learning for Goal-Oriented Dialogues"](http://ailab.kaist.ac.kr/papers/JLK2020)

## Requirements
All code was developed with [Google Cloud Platform(GCP)](https://cloud.google.com/) and [HTCondor](https://research.cs.wisc.edu/htcondor/). We reccomend to set up the HTCondor and environment on your GCP account to run the experiment in parallel.

To install requirements:

```sh
conda env create -f environment.yml
conda activate badp-rl
```

## Bayes-Adaptive Dialogue Planning (BADP)

To run the data collection with BADP in the paper, run this command:

```sh
python selfplay.py
```

## Policy improvement via Bayes-Adaptive Dialogue Planning (BADP-RL)

To run the policy improvement with collected data, run this command:

```sh
python train.py
```

## Citation

If this repository helps you in your academic research, you are encouraged to cite our paper. Here is an example bibtex:
```bibtex
@article{Jang_Lee_Kim_2020,
  title={Bayes-Adaptive Monte-Carlo Planning and Learning for Goal-Oriented Dialogues},
  journal={Proceedings of the AAAI Conference on Artificial Intelligence},
  author={Jang, Youngsoo and Lee, Jongmin and Kim, Kee-Eung},
  year={2020},
}
```

## Acknowledgement
This code is adapted and modified upon the code [github](https://github.com/facebookresearch/end-to-end-negotiator) of EMNLP 2017 paper ["Deal or No Deal? End-to-End Learning for Negotiation Dialogues"](https://arxiv.org/pdf/1706.05125.pdf) and ICML 2018 paper ["Hierarchical Text Generation and Planning for Strategic Dialogue"](https://arxiv.org/pdf/1712.05846.pdf). We appreciate their released dataset and code which are very helpful to our research.

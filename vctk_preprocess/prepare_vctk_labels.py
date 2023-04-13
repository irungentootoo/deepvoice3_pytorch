# coding: utf-8
"""
Prepare HTS alignments for VCTK.

usage: prepare_vctk_labels.py [options] <data_root> <out_dir>

options:
    -h, --help               Show help message.
"""
from docopt import docopt
import os
from nnmnkwii.datasets import vctk
from os.path import join, exists, splitext, basename
import sys
from glob import glob

from subprocess import Popen, PIPE
from tqdm import tqdm


def do(cmd):
    print(cmd)
    p = Popen(cmd, shell=True)
    p.wait()


if __name__ == "__main__":
    args = docopt(__doc__)
    data_root = args["<data_root>"]
    out_dir = args["<out_dir>"]

    for idx in tqdm(range(len(vctk.available_speakers))):
        speaker = vctk.available_speakers[idx]

        wav_root = join(data_root, f"wav48/p{speaker}")
        txt_root = join(data_root, f"txt/p{speaker}")
        assert exists(wav_root)
        assert exists(txt_root)
        print(wav_root, txt_root)

        # Do alignments
        cmd = f"python ./extract_feats.py -w {wav_root} -t {txt_root}"
        do(cmd)

        # Copy
        lab_dir = join(out_dir, f"p{speaker}")
        if not exists(lab_dir):
            os.makedirs(lab_dir)
        cmd = f"cp ./latest_features/merlin/misc/scripts/alignment/phone_align/full-context-labels/mono/*.lab {lab_dir}"
        do(cmd)

        # Remove
        do("rm -rf ./latest_features")

    sys.exit(0)

#!/usr/bin/env python3
# coding: utf-8

import os
import argparse
from tools import load_media
from tools import generate_image_sequence
from tools import generate_image_sequence_timeline

if __name__ == '__main__':
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
    parser = argparse.ArgumentParser(description='DaVinci Resolve lipsync timeline generator runner')
    parser.add_argument(
        'resource_id',
        type=str,
        help='resource id',
    )
    args = parser.parse_args()
    output_kana_segment_sequence_path = os.path.normpath(os.path.join(SCRIPT_DIR, 'out', f'{args.resource_id}.csv'))
    load_media.main(args.resource_id)
    generate_image_sequence.main(args.resource_id, output_kana_segment_sequence_path)
    generate_image_sequence_timeline.main(args.resource_id, output_kana_segment_sequence_path)
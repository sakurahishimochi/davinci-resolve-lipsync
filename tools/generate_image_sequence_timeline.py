#!/usr/bin/env python3
# coding: utf-8

import os
import argparse
from enum import Enum
from .generate_image_sequence import KanaSegmentSequence
from .modules import kana_to_image_frames
from .modules import utils
from .modules.resources import RESOURCES

class ExitStatus(Enum):
    SUCCESS = 0

def main(resource_id, kana_segment_sequence_file_path):
    import DaVinciResolveScript as bmd
    resolve = bmd.scriptapp('Resolve')
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    media_pool = project.GetMediaPool()
    frame_rate = project.GetSetting('timelineFrameRate')
    num_timelines = project.GetTimelineCount()

    timeline_title = resource_id

    for timeline_order in range(1, num_timelines + 1):
        timeline_candidate = project.GetTimelineByIndex(timeline_order)
        timeline_candiadate_name = timeline_candidate.GetName()
        if timeline_candiadate_name == timeline_title:
            media_pool.DeleteTimelines([ timeline_candidate ])
            break

    audio_file_abspath = os.path.abspath(RESOURCES[resource_id]['audio'])
    image_file_basenames = [ os.path.basename(image_path) for image_path in RESOURCES[resource_id]['image'].values() ]

    media_pool_item_audio_file = None
    media_pool_item_image_files = []
    media_pool_root_folder = media_pool.GetRootFolder()
    media_pool_clip_list = media_pool_root_folder.GetClipList()
    for media_pool_clip in media_pool_clip_list:
        media_pool_clip_type = media_pool_clip.GetClipProperty('Type')
        candidate_audio_file_path = media_pool_clip.GetClipProperty('File Path')
        if media_pool_clip_type in [ 'オーディオ', 'Audio' ]:
            if audio_file_abspath == os.path.abspath(candidate_audio_file_path):
                media_pool_item_audio_file = media_pool_clip
        elif media_pool_clip_type in [ '複合', 'Composition' ]:
            if media_pool_clip.GetName() in image_file_basenames:
                media_pool_item_image_files.append(media_pool_clip)

    audio_file_duration_msec = utils.get_duration_msec(media_pool_item_audio_file)

    timeline = media_pool.CreateEmptyTimeline(timeline_title)
    project.SetCurrentTimeline(timeline)

    duration_frames = utils.get_duration_frames(media_pool_item_audio_file)
    media_pool.AppendToTimeline([{
        'mediaPoolItem': media_pool_item_audio_file,
        'startFrame': 0,
        'endFrame': duration_frames,
        'mediaType': 2,
    }])

    kana_segment_sequence = KanaSegmentSequence.load_file(kana_segment_sequence_file_path)
    image_frame_segments = kana_to_image_frames.construct_image_frame_segments(resource_id, kana_segment_sequence, frame_rate, audio_file_duration_msec)
    media_pool_item_image_frame_segments = [
        {
            'mediaPoolItem': next(
                filter(
                    lambda mpi: ifs.image_basename == mpi.GetName(),
                    media_pool_item_image_files
                ),
            ),
            'startFrame': ifs.begin_frame_idx,
            'endFrame': ifs.end_frame_idx,
            'mediaType': 1,
            'trackIndex': 1,
        }
        for ifs
        in image_frame_segments.data
    ]
    media_pool.AppendToTimeline(media_pool_item_image_frame_segments)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate image sequence timeline')
    parser.add_argument(
        'resource_id',
        type=str,
        help='resource id',
    )
    parser.add_argument(
        'kana_segment_sequence_file_path',
        type=str,
        help='kana segment sequence file path',
    )
    args = parser.parse_args()
    main(args.resource_id, args.kana_segment_sequence_file_path)
    exit(ExitStatus.SUCCESS.value)
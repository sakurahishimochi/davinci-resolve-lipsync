import random
import string
import argparse
from enum import Enum
import DaVinciResolveScript as bmd
from .modules.resources import RESOURCES
from .modules import utils

class ExitStatus(Enum):
    SUCCESS = 0

def main(resource_id):
    def generate_temporal_timeline_name(existing_timeline_names):
        class DuplicatedTimelineNameError(ValueError):
            pass

        expected_retry_count_max = 5
        temporal_timeline_name_length = 12
        for _ in range(0, expected_retry_count_max):
            try:
                timeline_name_candidate = ''.join(random.choices(string.ascii_letters, k=temporal_timeline_name_length))
                if timeline_name_candidate in existing_timeline_names:
                    raise DuplicatedTimelineNameError()
                return timeline_name_candidate
            except DuplicatedTimelineNameError:
                continue
        raise RuntimeError('Too many timeline name regeneration. Maybe something goes wrong.')

    resolve = bmd.scriptapp('Resolve')
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()

    frame_rate = project.GetSetting('timelineFrameRate')
    media_pool = project.GetMediaPool()

    existing_timelines = [ project.GetTimelineByIndex(timeline_idx) for timeline_idx in range(1, project.GetTimelineCount() + 1) ]
    existing_timeline_names = [ timeline.GetName() for timeline in existing_timelines ]

    timeline = media_pool.CreateEmptyTimeline(generate_temporal_timeline_name(existing_timeline_names))
    project.SetCurrentTimeline(timeline)

    media_pool_root_folder = media_pool.GetRootFolder()
    media_pool_clip_list = media_pool_root_folder.GetClipList()
    existing_composition_clips = filter(lambda mpc: mpc.GetClipProperty('Type') in [ '複合', 'Composition' ], media_pool_clip_list)
    existing_composition_clip_names = list(map(lambda ecc: ecc.GetClipProperty('Clip Name'), existing_composition_clips))

    media_pool_audio_clip = media_pool.ImportMedia([ RESOURCES[resource_id]['audio'] ])
    media_pool.AppendToTimeline(media_pool_audio_clip)
    media_pool_image_clips = media_pool.ImportMedia(list(RESOURCES[resource_id]['image'].values()))
    for track_idx, media_pool_image_clip in enumerate(media_pool_image_clips, 2):
        timeline_items = media_pool.AppendToTimeline([
            {
                'mediaPoolItem': media_pool_image_clip,
                'startFrame': 1,
                'mediaType': 1,
                'trackIndex': track_idx,
            }
        ])
        media_pool_image_clip_name = media_pool_image_clip.GetClipProperty('Clip Name')
        if media_pool_image_clip_name not in existing_composition_clip_names:
            timeline.CreateCompoundClip(
                timeline_items,
                {
                    'startTimecode': utils.convert_num_frames_to_timecode(0, frame_rate),
                    'name': media_pool_image_clip_name,
                }
            )

    media_pool.ImportMedia(RESOURCES[resource_id]['others'])

    if not media_pool.DeleteTimelines([ timeline ]):
        raise RuntimeError('Failed to delete temporal timeline')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load media')
    parser.add_argument(
        'resource_id',
        type=str,
        help='resource id',
    )
    args = parser.parse_args()
    main(args.resource_id)
    exit(ExitStatus.SUCCESS.value)

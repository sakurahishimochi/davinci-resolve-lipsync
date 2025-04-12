#!/usr/bin/env python3
# coding: utf-8

def get_duration_msec(media_pool_item):
    frame_rate = media_pool_item.GetClipProperty('FPS')
    duration_timecode = media_pool_item.GetClipProperty('Duration')
    hours, minutes, seconds, num_fraction_frames = map(lambda s: int(s), duration_timecode.split(':'))
    hours_msec = hours * 60 * 60 * 1000
    minutes_msec = minutes * 60 * 1000
    seconds_msec = seconds * 1000
    num_frames_msec = frame_rate / num_fraction_frames * 1000
    return hours_msec + minutes_msec + seconds_msec + num_frames_msec

def get_duration_frames(media_pool_item):
    frame_rate = media_pool_item.GetClipProperty('FPS')
    duration_timecode = media_pool_item.GetClipProperty('Duration')
    return convert_timecode_to_num_frames(duration_timecode, frame_rate)

def convert_num_frames_to_timecode(num_frames, frame_rate):
    num_hours_frames, remaining_num_frames = divmod(num_frames, 60 * 60 * frame_rate)
    num_minutes_frames, remaining_num_frames = divmod(remaining_num_frames, 60 * frame_rate)
    num_seconds_frames, num_fraction_frames = divmod(remaining_num_frames, frame_rate)
    return '{0:s}:{1:s}:{2:s}:{3:s}'.format(
        str(int(num_hours_frames)).zfill(2),
        str(int(num_minutes_frames)).zfill(2),
        str(int(num_seconds_frames)).zfill(2),
        str(int(num_fraction_frames)).zfill(2),
    )

def convert_timecode_to_num_frames(timecode, frame_rate):
    hours, minutes, seconds, num_fraction_frames = map(lambda s: int(s), timecode.split(':'))
    num_hours_frames = hours * 60 * 60 * frame_rate
    num_minutes_frames = minutes * 60 * frame_rate
    num_seconds_frames = seconds * frame_rate
    return num_hours_frames + num_minutes_frames + num_seconds_frames + num_fraction_frames


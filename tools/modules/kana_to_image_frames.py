#!/usr/bin/env python3
# coding: utf-8

from .resources import RESOURCES
from enum import Enum

class ImageFrame:
    class ImageFrameClass(Enum):
        VOWEL = 'vowel'
        CORONAL = 'coronal'
        OTHER = 'other'

    def __init__(self, frame_class, image_path, duration_msec = None):
        self.frame_class = frame_class
        self.image_path = image_path
        self.duration_msec = duration_msec

    def num_frames(self, fps):
        return fps * self.duration_msec / 1000


def get_image_frames(resource, kana):
    IMAGE_FRAME_A = ImageFrame(ImageFrame.ImageFrameClass.VOWEL, resource['image']['A'])
    IMAGE_FRAME_I = ImageFrame(ImageFrame.ImageFrameClass.VOWEL, resource['image']['I'])
    IMAGE_FRAME_U = ImageFrame(ImageFrame.ImageFrameClass.VOWEL, resource['image']['U'])
    IMAGE_FRAME_E = ImageFrame(ImageFrame.ImageFrameClass.VOWEL, resource['image']['E'])
    IMAGE_FRAME_O = ImageFrame(ImageFrame.ImageFrameClass.VOWEL, resource['image']['O'])
    IMAGE_FRAME_SHUT = ImageFrame(ImageFrame.ImageFrameClass.OTHER, resource['image']['SHUT'])
    IMAGE_FRAME_LABIAL = ImageFrame(ImageFrame.ImageFrameClass.OTHER, resource['image']['SHUT'], 50)
    IMAGE_FRAME_CORONAL_I = ImageFrame(ImageFrame.ImageFrameClass.CORONAL, resource['image']['CORONAL_I'], 50)
    IMAGE_FRAME_CORONAL_U = ImageFrame(ImageFrame.ImageFrameClass.CORONAL, resource['image']['CORONAL_U'], 50)
    IMAGE_FRAME_CORONAL = ImageFrame(ImageFrame.ImageFrameClass.CORONAL, resource['image']['CORONAL_SCHWA'], 50)
    IMAGE_FRAME_DORSAL = ImageFrame(ImageFrame.ImageFrameClass.OTHER, resource['image']['SCHWA'], 50)
    IMAGE_FRAME_W = ImageFrame(ImageFrame.ImageFrameClass.OTHER, resource['image']['U'], 50)
    IMAGE_FRAME_Y = ImageFrame(ImageFrame.ImageFrameClass.OTHER, resource['image']['I'], 50)

    if kana in [ 'a', ]:
        return [ IMAGE_FRAME_A ]
    elif kana in [ 'i' ]:
        return [ IMAGE_FRAME_I ]
    elif kana in [ 'u' ]:
        return [ IMAGE_FRAME_U ]
    elif kana in [ 'e' ]:
        return [ IMAGE_FRAME_E ]
    elif kana in [ 'o' ]:
        return [ IMAGE_FRAME_O ]
    elif kana in [ 'ka', 'ha', 'ga' ]:
        return [ IMAGE_FRAME_DORSAL, IMAGE_FRAME_A ]
    elif kana in [ 'ki', 'hi', 'gi' ]:
        return [ IMAGE_FRAME_DORSAL, IMAGE_FRAME_I ]
    elif kana in [ 'ku', 'hu', 'gu' ]:
        return [ IMAGE_FRAME_DORSAL, IMAGE_FRAME_U ]
    elif kana in [ 'ke', 'he', 'ge' ]:
        return [ IMAGE_FRAME_DORSAL, IMAGE_FRAME_E ]
    elif kana in [ 'ko', 'ho', 'go' ]:
        return [ IMAGE_FRAME_DORSAL, IMAGE_FRAME_O ]
    elif kana in [ 'n' ]:
        return [ IMAGE_FRAME_SHUT ]
    elif kana in [ 'sa', 'ta', 'na', 'ra', 'za', 'da' ]:
        return [ IMAGE_FRAME_CORONAL, IMAGE_FRAME_A ]
    elif kana in [ 'shi', 'chi', 'ni', 'ri', 'ji' ]:
        return [ IMAGE_FRAME_CORONAL_I, IMAGE_FRAME_I ]
    elif kana in [ 'su', 'tsu', 'nu', 'ru', 'zu' ]:
        return [ IMAGE_FRAME_CORONAL_U, IMAGE_FRAME_U ]
    elif kana in [ 'se', 'te', 'ne', 're', 'ze', 'de' ]:
        return [ IMAGE_FRAME_CORONAL, IMAGE_FRAME_E ]
    elif kana in [ 'so', 'to', 'no', 'ro', 'zo', 'do' ]:
        return [ IMAGE_FRAME_CORONAL, IMAGE_FRAME_O ]
    elif kana in [ 'ma', 'pa', 'ba', 'fa' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_A ]
    elif kana in [ 'mi', 'pi', 'bi', 'fi' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_I ]
    elif kana in [ 'mu', 'pu', 'bu', 'fu' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_U ]
    elif kana in [ 'me', 'pe', 'be', 'fe' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_E ]
    elif kana in [ 'mo', 'po', 'bo', 'fo' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_O ]
    elif kana in [ 'mya', 'pya', 'bya' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_Y, IMAGE_FRAME_A ]
    elif kana in [ 'myu', 'pyu', 'byu' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_Y, IMAGE_FRAME_U ]
    elif kana in [ 'myo', 'pyo', 'byo' ]:
        return [ IMAGE_FRAME_LABIAL, IMAGE_FRAME_Y, IMAGE_FRAME_O ]
    elif kana in [ 'ya', 'kya', 'sha', 'cha', 'nya', 'hya', 'rya', 'gya', 'ja' ]:
        return [ IMAGE_FRAME_Y, IMAGE_FRAME_A ]
    elif kana in [ 'yu', 'kyu', 'shu', 'chu', 'nyu', 'hyu', 'ryu', 'gyu', 'ju' ]:
        return [ IMAGE_FRAME_Y, IMAGE_FRAME_U ]
    elif kana in [ 'she', 'che', 'je' ]:
        return [ IMAGE_FRAME_Y, IMAGE_FRAME_E ]
    elif kana in [ 'yo', 'kyo', 'sho', 'cho', 'nyo', 'hyo', 'ryo', 'gyo', 'jo' ]:
        return [ IMAGE_FRAME_Y, IMAGE_FRAME_O ]
    elif kana in [ 'wo' ]:
        return [ IMAGE_FRAME_W, IMAGE_FRAME_O ]
    elif kana in [ 'wa' ]:
        return [ IMAGE_FRAME_W, IMAGE_FRAME_A ]
    elif kana in [ 'we' ]:
        return [ IMAGE_FRAME_W, IMAGE_FRAME_E ]
    elif kana in [ 'wo' ]:
        return [ IMAGE_FRAME_W, IMAGE_FRAME_O ]
    else:
        raise ValueError('unexpected kana {0:s}'.format(kana))


def msec_to_frame_idx(msec, frame_rate):
    import math
    return math.floor(msec * frame_rate / 1000)


class ImageFrameSegment:
    def __init__(self, frame_class, image_path, begin_frame_idx, end_frame_idx = None):
        import os
        self.frame_class= frame_class
        self.image_path = image_path
        self.image_basename = os.path.basename(image_path)
        self.begin_frame_idx = begin_frame_idx
        self.end_frame_idx = end_frame_idx


class ImageFrameSegments:
    def __init__(self, resource):
        self.data = []
        self.resource = resource

    def append_or_merge(self, image_frame_segment):
        if len(self.data) == 0:
            if image_frame_segment.begin_frame_idx != 0:
                self.append_or_merge(ImageFrameSegment(
                    ImageFrame.ImageFrameClass.OTHER,
                    self.resource['image']['SHUT'],
                    0,
                    image_frame_segment.begin_frame_idx,
                ))
            self.data.append(image_frame_segment)
        else:
            last_image_frame_segment = self.data[-1]
            assert(last_image_frame_segment.end_frame_idx <= image_frame_segment.end_frame_idx)
            if last_image_frame_segment.end_frame_idx < image_frame_segment.begin_frame_idx:
                self.append_or_merge(ImageFrameSegment(
                    ImageFrame.ImageFrameClass.OTHER,
                    self.resource['image']['SHUT'],
                    last_image_frame_segment.end_frame_idx,
                    image_frame_segment.begin_frame_idx,
                ))
                self.append_or_merge(image_frame_segment)
            elif last_image_frame_segment.end_frame_idx > image_frame_segment.begin_frame_idx:
                last_image_frame_segment_end_frame_idx = image_frame_segment.begin_frame_idx
                if last_image_frame_segment.begin_frame_idx > last_image_frame_segment_end_frame_idx:
                    self.data.pop()
                    self.append_or_merge(ImageFrameSegment(
                        image_frame_segment.frame_class,
                        image_frame_segment.image_path,
                        last_image_frame_segment.begin_frame_idx,
                        image_frame_segment.end_frame_idx,
                    ))
                else:
                    last_image_frame_segment.end_frame_idx = last_image_frame_segment_end_frame_idx
                    self.append_or_merge(image_frame_segment)
            else:
                if last_image_frame_segment.image_path == image_frame_segment.image_path:
                    last_image_frame_segment.end_frame_idx = image_frame_segment.end_frame_idx
                else:
                    self.data.append(image_frame_segment)

    def fill(self, image_path, duration_msec, frame_rate):
        if len(self.data) > 0:
            last_image_frame_segment = self.data[-1]
            start_frame_idx = last_image_frame_segment.end_frame_idx
        else:
            start_frame_idx = 0
        end_frame_idx = msec_to_frame_idx(duration_msec, frame_rate)
        if start_frame_idx < end_frame_idx:
            silent_image_frame_segment = ImageFrameSegment(
                ImageFrame.ImageFrameClass.OTHER,
                image_path,
                start_frame_idx,
                end_frame_idx,
            )
            self.append_or_merge(silent_image_frame_segment)

    def fill_silence(self, duration_msec, frame_rate):
        self.fill(self.resource['image']['SHUT'], duration_msec, frame_rate)


def construct_image_frame_segments(resource_id, kana_segment_sequence, frame_rate, duration_msec):
    resource = RESOURCES[resource_id]
    image_frame_segments = ImageFrameSegments(resource)
    for kana_segment in kana_segment_sequence.segments:
        image_frames = get_image_frames(resource, kana_segment.kana)
        if len(image_frames) == 1:
            image_frame = image_frames[0]
            assert(image_frame.duration_msec is None)
            image_frame_segments.append_or_merge(ImageFrameSegment(
                image_frame.frame_class,
                image_frame.image_path,
                msec_to_frame_idx(kana_segment.begin_msec, frame_rate),
                msec_to_frame_idx(kana_segment.end_msec, frame_rate),
            ))
        elif len(image_frames) == 2:
            first_image_frame = image_frames[0]
            assert(first_image_frame.duration_msec is not None)
            first_image_frame_segment_begin_msec = kana_segment.begin_msec - first_image_frame.duration_msec
            image_frame_segments.append_or_merge(ImageFrameSegment(
                first_image_frame.frame_class,
                first_image_frame.image_path,
                msec_to_frame_idx(first_image_frame_segment_begin_msec, frame_rate),
                msec_to_frame_idx(kana_segment.begin_msec, frame_rate),
            ))
            second_image_frame = image_frames[1]
            assert(second_image_frame.duration_msec is None)
            image_frame_segments.append_or_merge(ImageFrameSegment(
                second_image_frame.frame_class,
                second_image_frame.image_path,
                msec_to_frame_idx(kana_segment.begin_msec, frame_rate),
                msec_to_frame_idx(kana_segment.end_msec, frame_rate),
            ))
        elif len(image_frames) == 3:
            first_image_frame = image_frames[0]
            assert(first_image_frame.duration_msec is not None)
            first_image_frame_segment_begin_msec = kana_segment.begin_msec - first_image_frame.duration_msec
            image_frame_segments.append_or_merge(ImageFrameSegment(
                first_image_frame.frame_class,
                first_image_frame.image_path,
                msec_to_frame_idx(first_image_frame_segment_begin_msec, frame_rate),
                msec_to_frame_idx(kana_segment.begin_msec, frame_rate),
            ))
            second_image_frame = image_frames[1]
            assert(second_image_frame.duration_msec is not None)
            if second_image_frame.duration_msec > kana_segment.get_duration_msec():
                image_frame_segments.append_or_merge(ImageFrameSegment(
                    second_image_frame.frame_class,
                    second_image_frame.image_path,
                    msec_to_frame_idx(kana_segment.begin_msec, frame_rate),
                    msec_to_frame_idx(kana_segment.end_msec, frame_rate),
                ))
            else:
                second_image_frame_segment_end_msec = kana_segment.begin_msec + second_image_frame.duration_msec
                image_frame_segments.append_or_merge(ImageFrameSegment(
                    second_image_frame.frame_class,
                    second_image_frame.image_path,
                    msec_to_frame_idx(kana_segment.begin_msec, frame_rate),
                    msec_to_frame_idx(second_image_frame_segment_end_msec, frame_rate),
                ))
                third_image_frame = image_frames[2]
                assert(third_image_frame.duration_msec is None)
                image_frame_segments.append_or_merge(ImageFrameSegment(
                    third_image_frame.frame_class,
                    third_image_frame.image_path,
                    msec_to_frame_idx(second_image_frame_segment_end_msec, frame_rate),
                    msec_to_frame_idx(kana_segment.end_msec, frame_rate),
                ))
        else:
            raise('unexpected number of image frames')

    image_frame_segments.fill_silence(duration_msec, frame_rate)

    return image_frame_segments
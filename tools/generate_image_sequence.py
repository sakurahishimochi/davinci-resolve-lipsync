#!/usr/bin/env python3
# coding: utf-8

import os
import argparse
import mido
from enum import Enum
from .modules.resources import RESOURCES

class ExitStatus(Enum):
    SUCCESS = 0

class KanaSegmentSequence:
    class KanaSegmentCandidate:
        def __init__(self, kana, begin_msec):
            self.kana = kana
            self.begin_msec = begin_msec
        
        def finalize(self, end_msec):
            return KanaSegment(self.kana, self.begin_msec, end_msec)

    def __init__(self, segments = []):
        self.segments = segments
        self._candidates = {}

    def set_candidate(self, note_number, kana, begin_msec):
        assert(note_number not in self._candidates)
        self._candidates[note_number] = self.KanaSegmentCandidate(kana, begin_msec)

    def finalize_candidate(self, note_number, end_msec):
        assert(note_number in self._candidates)
        self.segments.append(self._candidates.pop(note_number).finalize(end_msec))

    def save_file(self, file_path):
        output_dir = os.path.dirname(file_path)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        with open(file_path, 'wt', encoding='utf-8') as f:
            for segment in self.segments:
                f.write(segment.to_data_entry_string())
    
    @classmethod
    def load_file(kls, file_path):
        with open(file_path, 'rt', encoding='utf-8') as f:
            return kls([ KanaSegment.from_data_entry_string(line) for line in f ])


class KanaSegment:
    def __init__(self, kana, begin_msec, end_msec):
        if isinstance(begin_msec, str):
            begin_msec = int(begin_msec)
        if isinstance(end_msec, str):
            end_msec = int(end_msec)
        assert(begin_msec < end_msec)
        self.kana = kana
        self.begin_msec = begin_msec
        self.end_msec = end_msec

    def get_duration_msec(self):
        return self.end_msec - self.begin_msec

    def to_data_entry_string(self):
        return '{0:s},{1:d},{2:d}\n'.format(self.kana, self.begin_msec, self.end_msec)

    @classmethod
    def from_data_entry_string(kls, string):
        return kls(*string.strip().split(','))


class KanaStream:
    def __init__(self, kana_sequence):
        self.read_idx = 0
        self.kana_sequence = kana_sequence
        self.kana_sequence_length = len(self.kana_sequence)

    def read(self):
        if self.read_idx >= self.kana_sequence_length:
            return None
        kana = self.kana_sequence[self.read_idx]
        self.read_idx += 1
        return kana


def main(resource_id, output_kana_segment_sequence_path):
    NOTE_ON_MESSAGE_TYPE = 'note_on'
    NOTE_OFF_MESSAGE_TYPE = 'note_off'
    SET_TEMPO_MESSAGE_TYPE = 'set_tempo'

    def _is_midi_note_message(message):
        return isinstance(message, mido.Message) and (message.type in (NOTE_ON_MESSAGE_TYPE, NOTE_OFF_MESSAGE_TYPE))

    def _is_set_tempo_message(message):
        return isinstance(message, mido.MetaMessage) and (message.type == SET_TEMPO_MESSAGE_TYPE)

    def _find_track_containing_notes(midi_tracks):
        for track in midi_tracks:
            for message in track:
                if _is_midi_note_message(message):
                    return track
        return None

    def _find_track_containing_set_tempo(midi_tracks):
        for track in midi_tracks:
            for message in track:
                if _is_set_tempo_message(message):
                    return track
        return None

    def _load_kana_sequence(kana_file_path):
        with open(kana_file_path, 'rb') as f:
            return [ line.decode().strip() for line in f ]

    def _get_tempo(tempo_track):
        for message in tempo_track:
            if _is_set_tempo_message(message):
                return message.tempo
        return None

    def _construct_kana_segment_sequence(midi_note_track, kana_stream, tick_to_msec):
        kana_segment_sequence = KanaSegmentSequence()
        last_message_time = 0
        for message in midi_note_track:
            current_message_time = last_message_time + message.time
            if _is_midi_note_message(message):
                if message.type == NOTE_ON_MESSAGE_TYPE:
                    kana = kana_stream.read()
                    print(kana, message.note, message.type)
                    kana_segment_sequence.set_candidate(message.note, kana, tick_to_msec(current_message_time))
                elif message.type == NOTE_OFF_MESSAGE_TYPE:
                    print(kana, message.note, message.type)
                    kana_segment_sequence.finalize_candidate(message.note, tick_to_msec(current_message_time))
            last_message_time = current_message_time
        return kana_segment_sequence

    midi_data = mido.MidiFile(RESOURCES[resource_id]['midi'])
    tempo_track = _find_track_containing_set_tempo(midi_data.tracks)
    midi_note_track = _find_track_containing_notes(midi_data.tracks)
    tempo = _get_tempo(tempo_track)
    tick_to_msec = (lambda tick: round(mido.tick2second(tick, midi_data.ticks_per_beat, tempo) * 1000))
    kana_sequence = _load_kana_sequence(RESOURCES[resource_id]['kana'])
    kana_stream = KanaStream(kana_sequence)
    kana_segment_sequence = _construct_kana_segment_sequence(midi_note_track, kana_stream, tick_to_msec)
    kana_segment_sequence.save_file(output_kana_segment_sequence_path)


if __name__ == '__main__':
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
    parser = argparse.ArgumentParser(description='Generate image sequence')
    parser.add_argument(
        'resource_id',
        type=str,
        help='resource id',
    )
    parser.add_argument(
        '-o', '--output_kana_segment_sequence_file_path',
        type=str,
        help='kana segment sequence file path',
        default=os.path.join(SCRIPT_DIR, 'out', 'kana_segment_sequence.csv'),
    )
    args = parser.parse_args()
    main(args.resource_id, args.output_kana_segment_sequence_file_path)
    exit(ExitStatus.SUCCESS.value)

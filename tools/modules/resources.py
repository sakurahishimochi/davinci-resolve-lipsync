#!/usr/bin/env python3
# coding: utf-8

from os import path, getcwd, chdir
import json

def load_resource_definition():
    current_dir = getcwd()
    chdir(path.abspath(path.join(path.dirname(__file__), '../../res')))
    raw_resource_definitions = json.loads(open('resources.json', 'rt', encoding='utf-8').read())
    resources = {}
    for id, raw_resource_definition in raw_resource_definitions.items():
        resources[id] = {
            'audio': path.abspath(path.normpath(raw_resource_definition['audio'])),
            'kana':  path.abspath(path.normpath(raw_resource_definition['kana'])),
            'midi':  path.abspath(path.normpath(raw_resource_definition['midi'])),
            'image': {
                'A':             path.abspath(path.normpath(raw_resource_definition['image']['A'])),
                'I':             path.abspath(path.normpath(raw_resource_definition['image']['I'])),
                'CORONAL_I':     path.abspath(path.normpath(raw_resource_definition['image']['CORONAL_I'])),
                'U':             path.abspath(path.normpath(raw_resource_definition['image']['U'])),
                'CORONAL_U':     path.abspath(path.normpath(raw_resource_definition['image']['CORONAL_U'])),
                'E':             path.abspath(path.normpath(raw_resource_definition['image']['E'])),
                'O':             path.abspath(path.normpath(raw_resource_definition['image']['O'])),
                'SCHWA':         path.abspath(path.normpath(raw_resource_definition['image']['SCHWA'])),
                'CORONAL_SCHWA': path.abspath(path.normpath(raw_resource_definition['image']['CORONAL_SCHWA'])),
                'SHUT':          path.abspath(path.normpath(raw_resource_definition['image']['SHUT'])),
            },
            'others': list(map(lambda p: path.abspath(path.normpath(p)), raw_resource_definition['others'])),
        }
    chdir(current_dir)
    return resources

RESOURCES = load_resource_definition()
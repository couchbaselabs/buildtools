#!/usr/bin/env python

# Create a manifest file from a staging directory

import sys
import os
import hashlib
import json
import stat


# Based on # https://stomp.colorado.edu/blog/blog/2010/10/22/on-python-stat-octal-and-file-system-permissions/ (2012-06-25)
def get_permission(path):
    """Returns the permission of a file."""
    return oct(stat.S_IMODE(os.stat(path).st_mode))

def gen_manifest(stage_dir):
    """Generate a manifest from a directory"""
    manifest = {'files': []}

    for root, dirs, files in os.walk(stage_dir):
        for file_ in files:
            fullpath = os.path.join(root, file_)
            contents = open(fullpath, 'rb').read()
            sha1 = hashlib.sha1(contents).hexdigest()
            filename = os.path.relpath(fullpath, stage_dir)
            mode = get_permission(fullpath)
            manifest['files'].append({'path': filename, 'sha1': sha1,
                                      'mode': mode})
    return manifest

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) != 2:
        print "Usage: genmanifest.py [directory]"
        return

    stage_dir = os.path.abspath(argv[1])
    #print "Creating manifest for", stage_dir

    if not os.path.exists(stage_dir):
        print "Error: directory not found"
        return

    manifest = gen_manifest(stage_dir)
    print json.dumps(manifest)


if __name__ == '__main__':
    sys.exit(main())

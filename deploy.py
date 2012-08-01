#!/usr/bin/env python

# Put all files from a staging directory into a depot
# @todo we should read the manifest file and only
#       upload the files listed there..
# @todo add support for none-filesystem-locations
# @todo we should verify that the sha1 of the uploaded
#       file match

import sys
import os
import hashlib
import shutil

def gen_depot(stage_dir, depot_dir):
    """Put files from staging directory into the depot"""

    for root, dirs, files in os.walk(stage_dir):
        for file_ in files:
            fullpath = os.path.join(root, file_)
            contents = open(fullpath, 'rb').read()
            sha1 = hashlib.sha1(contents).hexdigest()
            dest_file = os.path.join(depot_dir, sha1)
            # NOTE vmx 2012-06-25: Currently we just overwrite the file if it
            #     already exists
            shutil.copy(fullpath, dest_file)
            print "Copied ", fullpath, "to", dest_file

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if sys.platform == "win32":
        depot_dir = os.environ.get("COUCHBASE_DEPOT_DIR", "c:/depot/");
    else:
        depot_dir = os.environ.get("COUCHBASE_DEPOT_DIR", "/export/depot/");

    if (len(argv) < 2) or (len(argv) > 3):
        print "Usage: gendepot.py stage-directory [depot-directory]"
        return

    stage_dir = os.path.abspath(argv[1])

    if len(argv) == 3:
        depot_dir = os.path.abspath(argv[2])

    if not os.path.exists(stage_dir):
        print "Error: stage directory not found"
        return
    if not os.path.exists(depot_dir):
        print "Error: depot directory not found"
        return

    gen_depot(stage_dir, depot_dir)


if __name__ == '__main__':
    sys.exit(main())

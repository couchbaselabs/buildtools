#! /usr/bin/env python
# @todo install dependencies recursively
# @todo install the maifest file to "etc/packages"
# @todo check the mode on the installed file

import json
import sys
import hashlib
import os.path
import urllib
import exceptions

class ChecksumException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def processDependencies(deps):
    """Installs all the dependencies"""
    # @todo recursively grab the manifest and run it
    for k in deps:
        print k["package"]

def checkFile(file):
    """Check the sha1 of and installed file and verifies its permission"""
    fullpath = os.path.join(install_dir, file["path"])
    print "\rChecksumming " + fullpath + " "
    digest = hashlib.new("sha1")
    digest.update(open(fullpath, "rb").read())
    if digest.hexdigest() != file["sha1"]:
        raise ChecksumException("FATAL Incorrect SHA1")
    # @todo check the mode
    return True

def installFile(file):
    """Download the file from the depot and write it to the correct location"""
    src = os.path.join(depot, file["sha1"])
    dest = os.path.join(install_dir, file["path"])
    try:
        os.makedirs(os.path.dirname(dest))
    # It doesn't matter if directory already exists
    except OSError:
        pass
    print "Installing " + dest + " "
    urllib.urlretrieve(src, dest)
    os.chmod(dest, int(file["mode"], 8))
    if not checkFile(file):
        os._exit(os.EX_DATAERR)
    print "OK"

def processFiles(files):
    for f in files:
        fullpath = os.path.join(install_dir, f['path'])
        if os.path.exists(fullpath):
            checkFile(f)
        else:
            installFile(f)

def processDirectories(dirs):
    for d in dirs:
        if not os.path.exists(d["path"]):
            os.makedirs(d["path"], 0755)

def installPackage(manifestfile):
    file = open(manifestfile, "rb")
    manifest = json.load(file)
    try:
        if 'depends' in manifest:
            processDependencies(manifest["depends"])
        if 'dirs' in manifest:
            processDirectories(manifest["dirs"])
        if 'files' in manifest:
            processFiles(manifest["files"])
    except ChecksumException, e:
        sys.exit(e.value)



if __name__ == '__main__':
    if sys.platform == "win32":
        depot = os.environ.get("COUCHBASE_DEPOT_DIR", "file://c:/depot/");
    else:
        depot = os.environ.get("COUCHBASE_DEPOT_DIR", "file:///export/depot/");
    install_dir = os.path.abspath(sys.argv[2])
    installPackage(sys.argv[1])

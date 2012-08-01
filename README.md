Preamble
--------

Please see http://hub.internal.couchbase.com/confluence/display/cbeng/Building+Couchbase+Server+2.x

Example 1 - Snappy
------------------

* Compile Snappy:
  `./configure --prefix=/opt/couchbase`
  `gmake install DESTDIR=/tmp/snappy`

* Generate manifest file
  `python genmanifest.py /tmp/snappy/opt/couchbase > snappy-1.0.5-solaris32.json`

* Deploy the binaries to our software depot
  `python deploy.py /tmp/snappy/opt/couchbase`

* Install it to the directory named install
  `python populate.py snappy-1.0.5-solaris32.json install`

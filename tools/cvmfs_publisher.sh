#!/bin/bash

CVMFS_DIR=""

# Try to expand standard output
cat | tar -xz --no-same-owner --no-selinux --no-xattrs -C "${CVMFS_DIR}"


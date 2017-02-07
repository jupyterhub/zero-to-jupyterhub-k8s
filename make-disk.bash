#!/bin/bash

#
# Create a new disk, mount it to a new path, and return the path.
#

set -e

if [ -z "$1" ]; then
	echo Usage: $0 NAME
	exit 1
fi

NAME="$1"
TS="$(date '+%Y%m%d-%H%M%S')"
disk_name="${NAME}-${TS}"

gcloud compute disks create ${disk_name} --size 10 --type pd-ssd
gcloud compute instances attach-disk provisioner-01 --disk ${disk_name}

devpath="/dev/disk/by-id"
device=$(ls -rt ${devpath} | tail -1)
blkdev=${devpath}/${device}
mntpath="/mnt/disks/${disk_name}"

sudo mkfs.ext4 -F -E lazy_itable_init=0,lazy_journal_init=0,discard ${blkdev}
sudo mkdir -p ${mntpath}
sudo mount -o discard,defaults ${blkdev} ${mntpath}

echo ${mntpath}

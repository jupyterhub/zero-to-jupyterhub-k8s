#!/bin/bash

set -e

# Added EEG data
wget https://www.dropbox.com/s/n3hb7cqffjwhgy1/cogneuro88data.tar.gz
tar -xvf cogneuro88data.tar.gz
rm cogneuro88data.tar.gz

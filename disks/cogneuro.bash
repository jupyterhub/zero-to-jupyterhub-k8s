#!/bin/bash

set -e

# Added MOAR EEG data
wget https://www.dropbox.com/s/4f0ek79ytxwcgwx/cogneuro88data.tar.gz
tar -xvf cogneuro88data.tar.gz
rm cogneuro88data.tar.gz

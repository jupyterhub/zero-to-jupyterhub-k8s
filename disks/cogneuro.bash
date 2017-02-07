#!/bin/bash

set -e

wget https://www.dropbox.com/s/2ccxfwg6t5d2rfw/data.zip
unzip data.zip
rm -rf __MACOSX/
rm data.zip

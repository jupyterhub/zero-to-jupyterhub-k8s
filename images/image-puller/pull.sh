#!/bin/sh
# Script to talk to a docker daemon & pull a given image
#
# Takes all input in form of environment variables
#
# IMAGE_NAME
# Name of image to be pulling, without tag
# IMAGE_TAG
# Tag of the image to be pulling
# CURL_EXTRA_OPTIONS
# Extra commandline options to pass to curl
#
# Script expects a docker daemon unix socket with support for at least v1.23
# of the docker API in /var/run/docker.sock
#
# If IMAGE_NAME starts with 'gcr.io', the script will assume it is running on Google Cloud
# and it has access to the API metadata service to fetch credentials. Then it will fetch
# credentials and pull from that repository.
# In the future, this could be extended to other private image registries too.
# However, it means if you have a gcr.io *public* image and want to pull it anywhere not
# on Google Cloud, pulling will fail.
#
# Requires curl & jq to work
set -euo pipefail

# Allow setting additional curl options
CURL_EXTRA_OPTIONS=${CURL_EXTRA_OPTIONS:-}
CURL_OPTIONS="--fail --silent --show-error ${CURL_EXTRA_OPTIONS}"

# Stores auth info if needed
AUTH=""

case ${IMAGE_NAME} in gcr.io*)
    echo "Image hosted on gcr.io, assuming we are running on Google Cloud..."
    # Assume we are on google cloud, use metadata service to fetch pulling credentials
    PASSWORD=$(curl -s -f -m 10 "http://metadata/computeMetadata/v1/instance/service-accounts/default/token" -H "Metadata-Flavor: Google" \
                | jq -r .access_token)

    # This is the format for making the authentication token for docker registry from a username + password
    AUTH=$(echo -n "{\"username\": \"_token\", \"email\": \"notval@goo.com\", \"password\": \"${PASSWORD}\"}" \
                | base64 \
                | tr -d '\n')
esac

# We expect at least v1.23 of the docker API to be present, which is fairly old by now.
# Since these do not get actively removed, we should be fine for a while
echo "Pulling image ${IMAGE_NAME}:${IMAGE_TAG}..."

curl \
    -H "X-Registry-Auth: ${AUTH}" \
    -X POST \
    --unix-socket /var/run/docker.sock \
    ${CURL_OPTIONS} \
    "http:/v1.23/images/create?fromImage=${IMAGE_NAME}&tag=${IMAGE_TAG}"

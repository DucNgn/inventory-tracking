#!/bin/bash

# This script checks if the container was built.
# If it was, run tests inside the container.
# Otherwise, run tests on local.
# Running tests on local requires the main app started at local port 8000 (refers to README.md for instructions).

CONTAINER_NAME='inventory_api'
TEST_CMD='py.test app/tests'

if [ "$(docker ps -a | grep ${CONTAINER_NAME})" ];
then
    docker exec inventory_api /bin/sh -c ${TEST_CMD}
else
    ${TEST_CMD}
fi

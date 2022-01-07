#!/bin/bash
py.test app/tests/integration/api_v1/tavern_tests/test_*.tavern.yaml
py.test app/tests/crud

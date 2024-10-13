#!/usr/bin/env bash
set -e

# Run will produce output at /tmp/act-artifacts/1/...
# Remaining part dependent on 'actions/upload-artifact@v4' NAME.
# Uploads are ALWAYS .zip
gh act --artifact-server-path /tmp/act-artifacts --var ACT_LOCAL='true'
# gh act --artifact-server-path /tmp/act-artifacts --var-file vars_run_act

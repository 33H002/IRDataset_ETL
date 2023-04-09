#!/bin/sh

SENTRY_RELEASE=$(git rev-parse HEAD)
export SENTRY_RELEASE

python facebook_ad_insights_extra_collect.py
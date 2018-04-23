#!/usr/bin/env bash

sudo su postgres
psql -c 'SELECT version();'

#!/usr/bin/env bash

a=$(which go)
b=$(echo "$(which go)")

echo "
$a
$b
"
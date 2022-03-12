#!/bin/bash
value=`cat save_pid.txt`
echo "$value"
kill -9 "$values"
rm save_pid.txt
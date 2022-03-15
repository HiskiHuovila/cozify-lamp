#!/bin/bash
value=`cat save_pid.txt`
echo "$value"
kill "$value"
rm save_pid.txt
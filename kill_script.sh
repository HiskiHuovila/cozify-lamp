#!/cozify-lamp
value=`cat save_pid.txt`
kill "$value"
rm save_pid.txt

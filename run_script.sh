#!/cozify-lamp
nohup python3 test.py > my.log 2>&1 & 
echo $! > save_pid.txt
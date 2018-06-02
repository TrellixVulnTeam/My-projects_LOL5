# coin-sorter-raspberry

### installation step for pyuf package
* extraxt pyuf-master-package-modified(Base_mod_working_one).zip
* <pre> cd pyuf-master</pre>
* <pre > python3 setup.py install </pre>

### RUN Coin Sorter instruction

1.connect the uarm using usb

2.conncet camer (USB or ip_cam) (close other apps using camera ,it may lead conflict to accessing camera)

* if you using usb camera change <pre>url = 1 in line 25 </pre>
* if you using Ip camera change <pre>url ="http://192.168.2.110:8080" in line 25</pre>
  
 


3.run the command below to start

<pre>
cd blob
python3 coin_sorter.py
</pre>

#### if "port not found, current filter: {'hwid': 'USB VID:PID=2341:0042'}, all ports:" error accors
<pre>
 kindly verify Uarm is on and connected, restart Uarm
</pre>

#### if permission error accors run below code 
</pre>
<pre>
sudo chmod -R 777 /dev/
</pre>




							REGARDING THE UARM SWIFT PROJECT

Files Included :

1) There exists an another zip folder names pyuf-master-mod1.zip which contains the modified pyuf package

2) There is an also an another zip file named as pyuf-master-package-modified(Base_mod_working_one).zip which is also an modified pyuf package
  Note: First use package mentioned in step 1 and if it doesn't work then use the package mentioned in step 2.

3)Step to be followed before installing pyuf package:

   >Before installing pyuf package first we must install pyserial package 

   >Install pyserial using the command sudo pip install pyserial

   >After installing pyserial using pip now let's install pyuf package

   >Package installation steps are same for zip file in step1 or step2

   >First unzip the zip files mentioned in step1(if that zip fles fails use zip file in step2)
 
   >Go to the location where you unzipped the pyuf package zip file and you could see a single folder starting with name as 'pyuf...'

   >Move inside that folder and you could see a setup.py file 

   >Now run the python file using command python3 setup.py install

   >If installation proceeds without any errors then pyuf package has been installed successfully

4)Then after package installation the code to connect to UARM and make to control it's movement and pump action is given by the name armmove.py.
  Run this to control UARM

5)Then the code for processing the video_feed from webcamera is given by name coindetectvideodemo2.py and the code for processing the single image is givent by the name as coindetectimagedemo1.py







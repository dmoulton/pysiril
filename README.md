# pysiril
Pysiril scripts to automate siril 

## prepare.py
This script puts all the image and support files into directories where the script, and the Siril GUI expect them.

After running, you should have directories for flats, biases, darks, and a directory of lights for each object imaged. The script can only account for one set of each type of support file.

```
python prepare.py <directory to modify>
```  

## pre_process.py

Will process a directory that has been set up with the prepare.py script above.
Currently uses sigma clipping 

```  
python pre_process.py <directory name>
```

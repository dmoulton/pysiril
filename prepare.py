import sys
import os
import shutil
import re

def organize_support_files(work_dir,partial_name,destination):
    support_dir = os.path.join(work_dir,destination)

    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if partial_name in file:
                os.makedirs(support_dir, exist_ok=True)
                source_path = os.path.join(root, file)
                destination_path = os.path.join(support_dir, file)
                shutil.move(source_path, destination_path)
                print(f"File '{file}' moved to '{destination_path}'.")

def organize_object_dirs(work_dir):
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if 'Light' in file:

                #extract the object name from the Light_ filename
                start_of_name = r"Light_"
                end_of_name = r"_\d+\.\d+secs_\d+\.fit"
                start_removed = re.sub(start_of_name, "", file)             
                object_name = re.sub(end_of_name, "", start_removed)
                object_path = os.path.join(work_dir,file)

                #create a directory for the object and move the light files there
                new_object_dir = os.path.join(work_dir,object_name)
                new_object_lights_dir = os.path.join(work_dir,object_name,'lights')
                os.makedirs(new_object_lights_dir, exist_ok=True)
                shutil.move(object_path,new_object_lights_dir)

                print(f"File '{file}' moved to '{new_object_dir}'")

                #Create the needed symbolic links to support files
                #the source directory for the specific support files must already exist
                for subdir in ['flats','darks','biases']:
                    if (not os.path.exists(os.path.join(new_object_dir,subdir)) and 
                        os.path.exists(os.path.join(work_dir,subdir))):
                        os.symlink(os.path.join(work_dir,subdir), os.path.join(new_object_dir,subdir))
                        print(f"Created {subdir} links for {object_name}")


work_dir = os.path.abspath(sys.argv[1])

organize_support_files(work_dir,'Flat','flats')
organize_support_files(work_dir,'Dark','darks')
organize_support_files(work_dir,'Bias','biases')

organize_object_dirs(work_dir)

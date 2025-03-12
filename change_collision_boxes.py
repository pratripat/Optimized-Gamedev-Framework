# make a python program to load the folder data/configs/collision_boxes and make each file in the folder a dictionary with the key being the name of the file and the value being the contents of the file. Return the dictionary as the output of the function and save the given new data in a file named as the folder opened in data/configs/collision_boxes_updated folder.

# Input
# The input will be the path of the folder data/configs/collision_boxes.
import os
import json

def change_collision_boxes(path):
    data = {}
    # here we are iterating over the folders in the folder collision_boxes
    for folder in os.listdir(path):
        data[folder] = {}
        for file in os.listdir(path+'/'+folder):
            # here we are opening each file and storing the contents in the dictionary with the key as the name of the
            with open(path+'/'+folder+'/'+file, 'r') as f:
                data[folder][file] = json.load(f)
    
    return data

# path = 'data/configs/collision_boxes'
# data = change_collision_boxes(path)
# if not os.path.exists('data/configs/collision_boxes_updated'):
#     os.makedirs('data/configs/collision_boxes_updated')

# with open('data/configs/collision_boxes_updated/data.json', 'w') as f: 
#     f.write(json.dumps(data, indent=4))
# print(data)
# Output
# The output will be a dictionary with the key being the name of the file and the value being the contents of the file. The dictionary will be saved in a file named as the folder opened in data/configs/collision_boxes_updated folder.
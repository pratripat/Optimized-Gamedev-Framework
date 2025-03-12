import json, os

path = 'data/graphics/folder_animations/'

order = ['idle', 'idleflipped', 'moving', 'movingflipped', 'shoot', 'shootflipped', 'damage', 'damageflipped', 'death', 'deathflipped']
data = {}
for entity in os.listdir(path):
    data[entity] = {}
    for animation_id in order:
        animation_ids = [folder.split('_')[-1] for folder in os.listdir(path+'/'+entity)]
        if animation_id in animation_ids:
            f = open(path+'/'+entity+'/'+entity+'_'+animation_id+'/config.json', 'r')
            config_data = json.load(f)

            data[entity][animation_id] = config_data

f = open('data/graphics/animations/config.json', 'w')
f.write(json.dumps(data, indent=4))
f.close()
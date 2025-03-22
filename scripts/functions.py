import pygame, os, json, math

default_colorkey = (0, 0, 0)
filepath_exceptions = {'json'}

collison_boxes_path = 'data/configs/collision_boxes.json'
COLLISION_BOXES = json.load(open(collison_boxes_path))
INITIAL_WINDOW_SIZE = (1200, 600)
SCALE = 3

# Loading the image from the filepath
def load_image(filepath, colorkey=default_colorkey, scale=1):
    image = pygame.image.load(filepath).convert()
    image.set_colorkey(colorkey)

    # Only calling the resize function really needed to
    if scale != 1:
        image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))

    return image

def load_images_from_folder(folder_path, filepath_exceptions=filepath_exceptions):
    images = []

    # Getting all the filepaths
    paths = []
    for file in os.listdir(folder_path):
        # Making sure that no file has a file extension that we do not want to load, here we only want to load images so checking that files are pngs itself
        file_extension = file.split('.')[-1]
        if file_extension != 'png':
            if file_extension not in filepath_exceptions:
                error_messages = [
                    'Error from the "load_images in the functions.py"',
                    f'Filepath {file} is in the folder {folder_path} which was asked to load images',
                    'Ignoring this file n loading the rest'
                ]
                error_message(error_messages)

            continue

        paths.append(file)


    def path_sorter(path):
        return int(path.split('.')[0])

    for file in sorted(paths, key=path_sorter):
        #loading the image
        images.append(load_image(folder_path+'/'+file))

    return images

def load_images_from_spritesheet(filepath, scale=1):
    #Tries to load the file
    try:
        spritesheet = load_image(filepath)
    except Exception as e:
        print('LOADING SPRITESHEET ERROR: ', e, f':- {filepath}')
        return []

    rows = []
    images = []

    for y in range(spritesheet.get_height()):
        pixil = spritesheet.get_at((0, y))
        if pixil[2] == 255:
            rows.append(y)

    for row in rows:
        for x in range(spritesheet.get_width()):
            start_position = []
            pixil = spritesheet.get_at((x, row))
            if pixil[0] == 255 and pixil[1] == 255 and pixil[2] == 0:
                start_position = [x+1, row]
                width = height = 0

                for rel_x in range(start_position[0], spritesheet.get_width()):
                    pixil = spritesheet.get_at((rel_x, start_position[1]))
                    if pixil[0] == 255 and pixil[1] == 0 and pixil[2] == 255:
                        width = rel_x - start_position[0]
                        break

                for rel_y in range(start_position[1], spritesheet.get_height()):
                    pixil = spritesheet.get_at((start_position[0], rel_y))
                    if pixil[0] == 255 and pixil[1] == 0 and pixil[2] == 255:
                        height = rel_y - start_position[1]
                        break

                image = pygame.Surface((width, height))
                image.convert()
                image.set_colorkey((0,0,0))
                image.blit(spritesheet, (-start_position[0], -start_position[1]))

                if scale != 1:
                    image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))

                images.append(image)

    return images

# Make sure pygame is initialized and there is a screen
def convert_folder_to_spritesheet(path):
    animations = {}

    for animation_folder in os.listdir(path):
        images = load_images_from_folder(path+'/'+animation_folder)

        animations[animation_folder.split('_')[-1]] = images

    order = ['idle', 'idleflipped', 'moving', 'movingflipped', 'shoot', 'shootflipped', 'damage', 'damageflipped', 'death', 'deathflipped']

    animation_spritesheets = []
    max_width = 0
    total_height = 0

    for animation_id in order:
        if animation_id not in animations: continue

        images = animations[animation_id]
        image_surfaces = []

        total_width = 0
        max_height = 0
        for image in images:
            width, height = image.get_size()

            total_width += width+2
            if height+1 > max_height:
                max_height = height+1

            image_surface = pygame.Surface((width+2, height+1))

            # yellow to mark the beginning of the image
            image_surface.set_at((0, 0), (255, 255, 0))
            image_surface.set_at((width+1, 0), (255, 0, 255))
            image_surface.set_at((1,height), (255, 0, 255))

            image_surface.blit(image, (1,0))

            image_surfaces.append(image_surface)

        if total_width+1 > max_width:
            max_width = total_width+1
        total_height += max_height

        animation_spritesheet = pygame.Surface((total_width+1, max_height))
        animation_spritesheet.set_at((0, 0), (0, 0, 255))
        posx = 1
        for image in image_surfaces:
            animation_spritesheet.blit(image, (posx, 0))
            posx += image.get_width()

        animation_spritesheets.append(animation_spritesheet)

    spritesheet = pygame.Surface((max_width, total_height))
    posy = 0
    for animation_spritesheet in animation_spritesheets:
        spritesheet.blit(animation_spritesheet, (0,posy))
        posy += animation_spritesheet.get_height()

    pygame.image.save(spritesheet, f'{path.split("/")[-1]}.png')

def normalize_vector(vector, desired_magnitude_squared=1):
    magnitude_squared = vector[0]**2+vector[1]**2

    # no normalizing needed if it is already normalized
    if desired_magnitude_squared == magnitude_squared:
        return vector

    # only if there is a need for normalizing, it is done
    if magnitude_squared > 0:
        return [vector[0] * math.sqrt(desired_magnitude_squared/magnitude_squared), vector[1] * math.sqrt(desired_magnitude_squared/magnitude_squared)]

    return [0, 0]

# Makes the error more readible for later
def error_message(error_messages):
    print('\n\n===================================================\n\n')
    print('ERROR:-')
    for msg in error_messages:
        print(msg)
    print('\n\n===================================================\n\n')

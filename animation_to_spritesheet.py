import pygame, os 
from scripts.functions import load_images_from_folder

def convert_folder_to_spritesheet(path):
    pygame.init()
    screen = pygame.display.set_mode((10,10))

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

    # pygame.image.save(spritesheet, f'{path.split("/")[-1]}.png')

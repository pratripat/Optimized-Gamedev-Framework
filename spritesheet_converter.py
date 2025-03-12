import pygame

# def convert_to_new_spritesheet(spritesheet_filepath):
#     spritesheet = pygame.image.load(spritesheet_filepath).convert()
#     spritesheet.set_colorkey((0, 0, 0))

#     pygame.image.save(spritesheet, 'converted.png')

#     y1 = None
#     y2 = None

#     images = []
#     height = 0

#     for y in range(spritesheet.get_height()):
#         color = spritesheet.get_at((0, y))

#         if (color[0] == 0 and color[1] == 0 and color[2] == 255) or y == spritesheet.get_height()-1:
            
#             if y1 == None:
#                 y1 = y
#             elif (y2 == None) or y == spritesheet.get_height()-1: 
#                 y2 = y+1
#                 image = pygame.Surface((spritesheet.get_width(), y2-y1-1))
#                 height += y2-y1-1

#                 image.blit(spritesheet, (0, y1-1))

#                 image.set_at((0, 0), (0, 0, 255))
#                 image.set_at((1, 0), (255, 255, 0))

#                 for x in range(2, spritesheet.get_width()-1):
#                     color = spritesheet.get_at((x, 1))
#                     if color[0] == 255 and color[1] == 0 and color[2] == 255:
#                         image.set_at((x+1, 0), (255, 255, 0))
                
#                 images.append(image)

#                 y1 = y2
#                 y2 = None
        
#     new_spritesheet = pygame.Surface((spritesheet.get_width(), height))
#     y = 0
#     for image in images:
#         new_spritesheet.blit(image, (0, y))
#         y += image.get_height()
    
#     pygame.image.save(new_spritesheet, 'trial.png')

def load_images_from_spritesheet(filename):
    #Tries to load the file
    try:
        spritesheet = pygame.image.load(filename).convert()
    except Exception as e:
        print('LOADING SPRITESHEET ERROR: ', e, f':- {filename}')
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
                start_position = [x+1, row+1]
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

                images.append(image)

    return images

def convert_to_new_spritesheet(spritesheet_filepath):
    spritesheet = pygame.image.load(spritesheet_filepath).convert()
    spritesheet.set_colorkey((0, 0, 0))

    images = load_images_from_spritesheet(spritesheet_filepath)

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
    
    new_spritesheet = pygame.Surface((total_width+1, max_height))
    new_spritesheet.set_at((0, 0), (0, 0, 255))
    posx = 1
    for image in image_surfaces:
        new_spritesheet.blit(image, (posx, 0))
        posx += image.get_width()
    
    pygame.image.save(new_spritesheet, 'trial.png')
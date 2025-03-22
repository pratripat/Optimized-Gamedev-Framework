# load a file and make pygame images of size 32 by 32 from the tileset and make it into a spritesheet according to the format from the spritesheet_converter file

import pygame

COLORS = {
    (114, 117, 27, 255): (62, 137, 72),
    (104, 111, 22, 255): (38, 92, 66),
    (101, 108, 23, 255): (38, 92, 66),
    (99, 105, 23, 255): (38, 92, 66),
    (120, 123, 33, 255): (17, 171, 36),
    (127, 129, 36, 255): (99, 199, 77),
    (127, 130, 38, 255): (99, 199, 77),
    (179, 176, 169, 255): (255, 255, 255),
    (156, 168, 173, 255): (192, 203, 220),
    (198, 167, 64, 255): (254, 174, 52),
    (162, 129, 79, 255): (215, 118, 67)
}

def convert_pallete(image):
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            color = tuple(image.get_at((x, y)))
            print(color)
            if color in COLORS:
                image.set_at((x, y), COLORS[color])

    return image

def check_empty(image):
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            if image.get_at((x, y)) != (0, 0, 0):
                return False
    return True

def load_images_from_spritesheet(filename):
    try:
        tileset = pygame.image.load(filename).convert()
    except Exception as e:
        print(e)
        print('type filename again')
        return []
    
    images = []

    for y in range(0, tileset.get_height(), 32):
        for x in range(0, tileset.get_width(), 32):
            image = pygame.Surface((32, 32)).convert()
            image.fill((0, 0, 0))
            image.set_colorkey((0, 0, 0))
            image.blit(tileset, (0, 0), (x, y, 32, 32))
            # image = convert_pallete(image)
            if not check_empty(image):
                images.append(image)
    
    print(images)

    return images

def convert_to_spritesheet(images):
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

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((100, 100))

    while True:
        filename = input('Enter the filename (e -> exit): ')
        if filename == 'e': break
        images = load_images_from_spritesheet(filename)
        convert_to_spritesheet(images)
        print('done')
import pygame, os, json
from .functions import load_images_from_spritesheet, load_image

folder_path = 'data/graphics/animations'

class Animation_Handler:
    def __init__(self):
        self.animations = {}
        self.load_animations()

    def load_animations(self):
        config_data = json.load(open(folder_path+'/config.json', 'r'))

        for animation_spritesheet in os.listdir(folder_path):
            # making sure we are only loading the spritesheets and not the config file 
            extension = animation_spritesheet.split('.')[-1]
            if extension != 'png':
                continue

            # loading the configurations for the animation from the config file
            obj = animation_spritesheet.split('.')[0]
            config = config_data[obj]
            spritesheet_index = 0

            for animation_id in config:
                self.animations[obj + '_' + animation_id] = Animation_Data(folder_path + '/' + animation_spritesheet, config[animation_id], spritesheet_index)
                spritesheet_index += len(config[animation_id]['frames'])

    def get_animation(self, animation_id):
        animation_data = self.animations[animation_id]
        return Animation(animation_data)

class Animation_Data:
    def __init__(self, path, config, spritesheet_index):
        self.animation_path = path
        self.load_data(path, config, spritesheet_index)
    
    def load_data(self, path, config, spritesheet_index):
        images = load_images_from_spritesheet(path)[spritesheet_index:spritesheet_index + len(config['frames'])]
        if images == []: self.original_images = self.images = load_image(path) 
        else: self.original_images = self.images = images

        self.config = config

        # flips the images horizontally if required
        if self.config['flip']:
            self.images = [pygame.transform.flip(image, True, False) for image in self.images]

        self.resize_images(self.config['scale'])

    def resize_images(self, scale=1):
        if scale == 1: return

        self.images = [pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale)) for image in self.original_images]

    #Returns total number of frames of the animation
    def get_frames(self):
        return self.config['frames']

    #Returns all the frames in the form of images
    def get_images(self):
        return self.images

    #Returns the scale of the animation
    def get_scale(self):
        return self.config['scale']

    #Returns the time taken(in frames) to finish the animation
    def duration(self):
        return sum(self.config['frames'])


class Animation:
    def __init__(self, animation_data):
        self.animation_data = animation_data
        self.frame = 0
        self.load_image()
    
    # loads the image according to the current frame
    def load_image(self):
        frames = self.animation_data.get_frames()
        images = self.animation_data.get_images()
        self_frame = self.frame

        for i, frame in enumerate(frames):
            if self_frame > frame:
                self_frame -= frame
                continue
            
            self.image = images[i]
            break
    
    
    #Renders the current image
    def render(self, surface, position, flipped=[False, False], colorkey=(0,0,0), angle=0, center_rotation=True, alpha=None, animation_offset=None):
        offset = [0, 0]
        image = self.image

        if any(flipped):
            image = pygame.transform.flip(self.image, *flipped)
    
        if colorkey:
            image.set_colorkey(colorkey)

        if angle != 0:
            image_copy = image.copy()
            image = pygame.transform.rotate(image, angle)

            if center_rotation:
                offset[0] = image_copy.get_width()/2-image.get_width()/2
                offset[1] = image_copy.get_height()/2-image.get_height()/2

        if self.animation_data.config['centered']:
            offset[0] -= image.get_width()//2
            offset[1] -= image.get_height()//2

        if alpha != None:
            alpha_surface = pygame.Surface(image.get_size())
            alpha_surface.convert_alpha()
            alpha_surface.set_colorkey((0, 0, 0))
            alpha_surface.set_alpha(alpha)
            alpha_surface.blit(image, (0, 0))
            image = alpha_surface

        if animation_offset != None:
            offset = animation_offset.copy()

            scale = self.animation_data.config['scale']
            offset[0] *= scale
            offset[1] *= scale

        surface.blit(image, (position[0]+offset[0], position[1]+offset[1]))

    #Updates the current frame according to delta time
    def run(self, dt):
        self.frame += dt*60*self.animation_data.config['speed']

        if type(self.animation_data.config['loop']) == type([]):
            loop_indexes = self.animation_data.config['loop']

            if self.frame > sum(self.animation_data.config['frames'][:loop_indexes[1]+1]):
                self.frame = sum(self.animation_data.config['frames'][:loop_indexes[0]+1])

        if self.frame > self.animation_data.duration():
            if self.animation_data.config['loop'] == True:
                self.frame = 0
            elif self.animation_data.config['loop'] == False:
                self.frame = self.animation_data.duration()

        self.load_image()

    def change_scale(self, scale):
        self.animation_data.resize_images(scale)
        self.animation_data.config['scale'] = scale
    
    #The current image
    @property
    def current_image(self):
        return self.image

    @property
    def over(self):
        return self.frame >= self.animation_data.duration()

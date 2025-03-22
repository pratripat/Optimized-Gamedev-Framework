import pygame, json
from .functions import load_image, load_images_from_spritesheet, SCALE

''' JSON FILE
[
    {layer_id: [pos, id, filepath_index, spritesheet_index, image_scale], ...},
    {tilemap_id: autotile_bool, ...}
]
'''

''' SELF.LAYERS
{layer_id: {chunk_pos: {tile_pos: [id, pos, image, filepath, spritesheetindex, imagescale]}}}
'''


class Tilemap:
    TILE_RES = 32*SCALE
    CHUNK_SIZE = 8

    def __init__(self, filename, updated_tilemap_filenames={}, layer_ids_for_chunk_images=[]):
        self.filename = filename
        self.layers = {}
        self.chunk_images = {}
        self.load(updated_tilemap_filenames, layer_ids_for_chunk_images)

    # loads all the tiles from the json file
    def load(self, updated_tilemap_filenames, layer_ids_for_chunk_images=[]):
        data = json.load(open(self.filename, 'r'))

        layers, tilemaps = data
        for layer_id, tiles in layers.items():
            self.layers[layer_id] = {}

            for tile_data in tiles:
                # POSITION, ID, FILEPATH_INDEX, SPRITESHEET_INDEX, IMAGE_SCALE
                position, id, filepath_index, spritesheet_index, image_scale = tile_data
                
                filepath = list(tilemaps.keys())[filepath_index]

                if spritesheet_index == None: image = load_image(filepath, scale=image_scale)
                else: image = load_images_from_spritesheet(filepath, image_scale)[spritesheet_index]

                chunk, chunk_position = self.get_chunk(layer_id, position)
                chunk[tuple(position)] = {
                    'id': id,
                    'chunk_position': chunk_position,
                    'layer_id': layer_id,
                    'filepath': filepath,
                    'image': image,
                    'rect': pygame.Rect(*position, *image.get_size()),
                    'spritesheet_index': spritesheet_index,
                    'scale': image_scale
                }
            
            # create chunk images for the layers that are needed
            if layer_id in layer_ids_for_chunk_images:
                self.create_chunk_images(layer_id)
    
    # this creates an image for each chunk so that we can render the chunks instead of the individual tiles
    def create_chunk_images(self, layer_id):
        self.chunk_images[layer_id] = {}
        for chunk_pos in self.layers[layer_id]:
            chunk = self.layers[layer_id][chunk_pos]
            chunk_image = pygame.Surface((self.TILE_RES*self.CHUNK_SIZE, self.TILE_RES*self.CHUNK_SIZE)).convert()
            chunk_image.set_colorkey((0,0,0))

            for tile_pos in chunk:
                tile = chunk[tile_pos]
                chunk_image.blit(tile['image'], (tile_pos[0]-chunk_pos[0], tile_pos[1]-chunk_pos[1]))
            
            self.chunk_images[layer_id][chunk_pos] = chunk_image
    
    # renders the tiles
    def render(self, display_surface, scroll, visible_tiles_data, layer_ids):
        for layer_id in layer_ids:
            if layer_id not in visible_tiles_data: continue
            for chunk_pos, chunk in visible_tiles_data[layer_id].items():
                display_surface.blit(self.chunk_images[layer_id][chunk_pos], [chunk_pos[0]-scroll.x, chunk_pos[1]-scroll.y])

    # returns the tiles, chunk_pos
    def get_chunk(self, layer_id, position):
        chunk_res = self.TILE_RES * self.CHUNK_SIZE
        chunk_position = ((position[0]//chunk_res)*chunk_res, (position[1]//chunk_res)*chunk_res)
        if chunk_position not in self.layers[layer_id]: 
            self.layers[layer_id][chunk_position] = {}

        return self.layers[layer_id][chunk_position], chunk_position # (tiles, chunk_pos)

    # returns the chunk positions of the neighbor chunks
    def get_neighbor_chunks(self, layer_id, chunk_position):
        neighbors = []
        for dir in [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]:
            new_position = [chunk_position[0]+self.TILE_RES*self.CHUNK_SIZE*dir[0], chunk_position[1]+self.TILE_RES*self.CHUNK_SIZE*dir[1]]
            _, neighbor_chunk_position = self.get_chunk(layer_id, new_position)
            neighbors.append(neighbor_chunk_position)
        return neighbors
    
    # returns the tiles of the neighbour tiles
    def get_neighbour_tiles(self, layer_id, tile_pos):
        neighbors = []
        for dir in [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]:
            new_position = [tile_pos[0]+self.TILE_RES*dir[0], tile_pos[1]+self.TILE_RES*dir[1]]
            tiles, chunk_position = self.get_chunk(layer_id, new_position)
            tile = tiles.get(tuple(new_position))
            if tile == None:
                continue
            neighbors.append(tile)
        return neighbors

    # returns the positions of all the chunks that are visible
    def get_visible_chunks(self, visible_rect, layer_ids=None):
        chunks = {}
        # layers = [layer for layer in self.layers.values()]
        if layer_ids != None:
            layers = [self.layers[layer_id] for layer_id in layer_ids if layer_id in self.layers]
        else:
            layers = list(self.layers.values())

        center = visible_rect.center
        for layer_id in layer_ids:
            _, chunk_position = self.get_chunk(layer_id, center)
            neighbors = self.get_neighbor_chunks(layer_id, chunk_position)

            chunks[layer_id] = [chunk_position, *neighbors]

        return chunks
    
    # returns all the visible tiles
    def get_visible_tiles(self, visible_rect, layer_ids=None):
        data = {}

        visible_chunks = self.get_visible_chunks(visible_rect, layer_ids)
        
        for layer_id, chunk_positions in visible_chunks.items():
            layer = self.layers[layer_id]
            data[layer_id] = {}
            for chunk_position in chunk_positions:
                if len(layer[chunk_position]) == 0: continue
                data[layer_id][chunk_position] = layer[chunk_position]

        return data
    
    # returns the layer
    def get_tiles_with_id(self, layer_id):
        chunks = self.layers[layer_id]
        tiles = {}

        for chunk_pos in chunks:
            tiles.update(chunks[chunk_pos])
        
        return tiles

    def get_on_grid_tile_position(self, position):
        return [position[0] // self.TILE_RES * self.TILE_RES, position[1] // self.TILE_RES * self.TILE_RES]
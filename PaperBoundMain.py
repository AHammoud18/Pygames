# Pygames!
# By Ali Hammoud

import pygame
pygame.init()

class Rubi(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.player = pygame.image.load('graphics/map.png').convert_alpha()
        self.rect = self.player.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 2


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed



class camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        # camera offset
        self.offset = pygame.math.Vector2()
        self.halfWidth = self.displaySurface.get_size()[0]//2
        self.halfHeight = self.displaySurface.get_size()[1]//2

        # zoom feature (if needed)
        self.zoomScale = 1
        self.internalSurfaceSize = (2000, 2000)
        self.internalSurface = pygame.Surface(self.surfaceSize, pygame.SRCALPHA)
        self.internalRect = self.internalSurface.get_rect(center= (self.halfWidth, self.halfHeight))
        self.internalSurfaceSizeVect = pygame.math.Vector2(self.internalSurfaceSize)
        self.internalOffset = pygame.math.Vector2()
        self.internalOffset.x = self.internalSurfaceSize[0]//2 - self.halfWidth
        self.internalOffset.y = self.internalSurfaceSize[1]//2 - self.halfHeight

        # map 
        self.mapSurface = pygame.image.load('graphics/map.png').convert_alpha()
        self.mapRect = self.mapSurface.get_rect(topleft = (0,0))

        # camera bounds
        self.cameraBorders = {'left':200, 'right':200, 'top':100, 'bottom':100}
        l,t = self.cameraBorders['left'], self.cameraBorders['top']
        w = self.displaySurface.get_size()[0] - (self.cameraBorders['left'] + self.cameraBorders['right'])
        h = self.displaySurface.get_size()[1] = (self.cameraBorders['top'] + self.cameraBorders['bottom'])
        self.cameraRect = pygame.Rect(l,t,w,h)

    # camera centers on player
    def centerOnPlayer(self, target):
        self.offset.x = target.rect.centerx - self.halfWidth
        self.offset.y = target.rect.centery = self.halfHeight

    def customDraw(self, player):
        self.centerOnPlayer(player)
        self.internalSurface.fill('white')

        # ground
        mapOffset = self.mapRect.topleft - self.offset + self.internalOffset
        self.internalSurface.blit(self.mapSurface, mapOffset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset + self.internalOffset
            self.internalSurface.blit(sprite.image, offsetPos)

        scaledSurf = pygame.transform.scale(self.interanlSurface, self.internalSurfaceSizeVect * self.zoomScale)
        scaledRect = scaledSurf.get_rect(center = (self.halfWidth, self.halfHeight))
        self.displaySurface.blit(scaledSurf, scaledRect)


class paperBound():

    def __init__(self):
        # setup window & map
        self.screen = pygame.display.set_mode((640, 480))
        self.displaySurface = pygame.display.get_surface()
        self.worldWidth, self.worldHeight = 1280, 720
        self.camera = camera
        #self.worldMap = pygame.surface((self.worldWidth, self.worldHeight))
        
        self.clock = pygame.time.Clock()
        self.Rubi = Rubi((300, 300), self.camera)
        self.running = True
        self.clock.tick(24)
        self.main()



    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Game Start
            self.screen.fill('white')
            self.camera.update()
            self.camera.customDraw(player=self.Rubi)
            pygame.display.flip()



paperBound()
pygame.quit()
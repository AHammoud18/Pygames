# Pygames!
# By Ali Hammoud

import pygame
pygame.init()



class MeiMei(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.map = cameraGroup()
        self.image = pygame.image.load('graphics/rubi.png').convert_alpha()
        self.spriteSheet = pygame.image.load('graphics/debugSprite2.png').convert_alpha()
        self.character = []
        self.character.append(self.idleAnim())
        #print(self.character)
        self.character.append(self.flyingAnim())
        self.rect = self.character[0][0].get_rect(center=pos)
        self.position = (0,0)
        #self.flippedPlayer = pygame.transform.flip(self.character[self.currentSprite], flip_x=False, flip_y=False)
        #self.player = self.flippedPlayer
        self.direction = pygame.math.Vector2()
        self.speed = 2
        self.speedBonus = 1
        self.isLeft = False
        self.isRight = False


    def idleAnim(self):
        spriteW, spriteH = 63,58
        numCol = 5
        numRow = 1
        spriteList = []
        for col in range(numCol):
            x = col * spriteW
            y = numRow * spriteH
            sprite = self.spriteSheet.subsurface(pygame.Rect(x, y, spriteW,spriteH))
            rect = sprite.get_rect(center=(0,0))
            scaledSprite = pygame.transform.scale(sprite, (rect.width*4,rect.height*4))
            spriteList.append(scaledSprite)
        return spriteList
    
    def flyingAnim(self):
        spriteW, spriteH = 63,58
        numCol = 5
        numRow = 2
        spriteList = []
        for col in range(numCol):
            x = col * spriteW
            y = numRow * spriteH
            sprite = self.spriteSheet.subsurface(pygame.Rect(x, y, spriteW,spriteH))
            rect = sprite.get_rect(center=(0,0))
            scaledSprite = pygame.transform.scale(sprite, (rect.width*4,rect.height*4))
            spriteList.append(scaledSprite)
        return spriteList

    def goingRight(self, spriteType):
        character = []
        for i,v in enumerate(self.character[spriteType]):
            character.append(pygame.transform.flip(self.character[spriteType][i], flip_x=True, flip_y=False))
        return character
    

    def goingLeft(self, spriteType):
        character = []
        for i,v in enumerate(self.character[spriteType]):
            character.append(pygame.transform.flip(self.character[spriteType][i], flip_x=True, flip_y=False))
        return character


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
            if self.isRight == False:
                self.character[0] = self.goingRight(0)
                self.character[1] = self.goingRight(1)
                self.isLeft = False
                self.isRight = True

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            if self.isLeft == False:
                self.character[0] = self.goingLeft(0)
                self.character[1] = self.goingLeft(1)
                self.isRight = False
                self.isLeft = True
        else:
            self.direction.x = 0
        
        if keys[pygame.K_LSHIFT]:
            tick = pygame.time.get_ticks()
            self.speed = 4
            print(tick//60)
            
        else:
            tick = 0
            self.speed = 2
        
        
    

    def update(self):

        self.input()
        self.rect.center += self.direction * (self.speed * self.speedBonus)
        
     
    

class cameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.animationDelay = 300
        # camera offset
        self.offset = pygame.math.Vector2()
        self.scaledRect = None
        self.halfWidth = self.displaySurface.get_size()[0]//2 #640
        self.halfHeight = self.displaySurface.get_size()[1]//2 #360
        self.lastTick = pygame.time.get_ticks()
        # zoom feature (if needed)
        self.zoomScale = 0.6
        self.frame = 0
        self.internalSurfaceSize = (2000, 2000)
        self.internalSurface = pygame.Surface(self.internalSurfaceSize, pygame.SRCALPHA)
        self.internalRect = self.internalSurface.get_rect(center= (self.halfWidth, self.halfHeight))
        self.internalSurfaceSizeVect = pygame.math.Vector2(self.internalSurfaceSize)
        self.internalOffset = pygame.math.Vector2()
        self.internalOffset.x = self.internalSurfaceSize[0]//2 - self.halfWidth # 360
        self.internalOffset.y = self.internalSurfaceSize[1]//2 - self.halfHeight # 640

        # map 
        self.mapSurface = pygame.image.load('graphics/map.png').convert_alpha()
        self.mapRect = self.mapSurface.get_rect(topleft = (0,0))

        # border (for debugging)
        self.borderSurface = pygame.image.load('graphics/border.png').convert_alpha()

        # camera bounds
        self.cameraBorders = {'left':200, 'right':200, 'top':100, 'bottom':100}
        l,t = self.cameraBorders['left'], self.cameraBorders['top']
        w = self.displaySurface.get_size()[0] - (self.cameraBorders['left'] + self.cameraBorders['right']) # 880
        h = self.displaySurface.get_size()[1] - (self.cameraBorders['top'] + self.cameraBorders['bottom']) # 520
        self.cameraRect = pygame.Rect(l,t,w,h)

        

    # camera centers on player
    def centerOnPlayer(self, target):
        self.offset.x = target.rect.centerx - self.halfWidth  # -502
        self.offset.y = target.rect.centery - self.halfHeight # -452
        

    def customDraw(self, player):
        keys = pygame.key.get_pressed()
        self.centerOnPlayer(player)
        self.internalSurface.fill('white')
        spriteType = 0
        # ground
        mapOffset = self.mapRect.topleft - self.offset + self.internalOffset # 862, 1092
        self.internalSurface.blit(self.mapSurface, mapOffset)
        self.internalSurface.blit(self.borderSurface, mapOffset)

        # add character to map
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            currentTick = pygame.time.get_ticks()
            offsetPos = sprite.rect.topleft - self.offset + self.internalOffset # 902, 852
            # iterate through sprites to create animation
            if currentTick - self.lastTick >= self.animationDelay:
                if self.frame < len(sprite.character[spriteType])-1:
                    self.frame += 1
                else:
                    self.frame = 0
                self.lastTick = currentTick

            if keys[pygame.K_LSHIFT] and keys[pygame.K_RIGHT]:
                spriteType = 1
            elif keys[pygame.K_LSHIFT] and keys[pygame.K_LEFT]:
                spriteType = 1
            else:
                spriteType = 0

            self.internalSurface.blit(sprite.character[spriteType][self.frame], offsetPos)

        

        scaledSurf = pygame.transform.scale(self.internalSurface, self.internalSurfaceSizeVect * self.zoomScale)
        scaledRect = scaledSurf.get_rect(center = (self.halfWidth, self.halfHeight))

        # Restrict the character within the map's boundaries       
        if sprite.rect.top < self.mapRect.top:
            sprite.rect.top = self.mapRect.top

        if sprite.rect.left < self.mapRect.left:
            sprite.rect.left = self.mapRect.left

        if sprite.rect.right > self.mapRect.right:
            sprite.rect.right = self.mapRect.right

        if sprite.rect.bottom > self.mapRect.bottom:
            sprite.rect.bottom = self.mapRect.bottom
        self.displaySurface.blit(scaledSurf, scaledRect)


class paperBound():

    def __init__(self):
        # setup window & map
        self.screen = pygame.display.set_mode((1280, 720))
        self.displaySurface = pygame.display.get_surface()
        self.worldWidth, self.worldHeight = 2000, 2000
        self.camera = cameraGroup()
        #self.worldMap = pygame.surface((self.worldWidth, self.worldHeight))
        self.spawnPos = (0, 0)
        self.clock = pygame.time.Clock()
        self.MeiMei = MeiMei(self.spawnPos,group=self.camera)
        self.running = True
        self.main()



    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # Game Start
            self.screen.fill('white')
            self.clock.tick(60)
            self.camera.update()
            self.camera.customDraw(player=self.MeiMei)
            pygame.display.flip()



paperBound()
pygame.quit()
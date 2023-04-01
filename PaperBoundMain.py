# Pygames!
# By Ali Hammoud

import pygame



class paperBound():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.main()


    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # Game Start
            self.screen.fill('white')
            pygame.display.flip()
            self.clock.tick(24)



paperBound()
pygame.quit()
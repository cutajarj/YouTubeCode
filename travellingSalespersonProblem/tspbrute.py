import pygame
import math
from itertools import permutations


class TSPSolver:
    def __init__(self, screen):
        self.screen = screen
        self.world_map = pygame.image.load('resouces/world-map-custom.png')
        self.marker = pygame.image.load('resouces/locationMarker.png')
        self.city_marker = pygame.transform.scale(self.marker, (34, 60))
        self.button_image = pygame.image.load('resouces/solveButton.png')
        self.button_rect = self.button_image.get_rect().move(100, 900)
        self.destinations = []
        self.clock = pygame.time.Clock()
        self.curr_perm = None
        self.solving = False
        self.shortest_distance = float("inf")
        self.shortest_permutation = None
        self.perms = None
        self.reset()

    def event_loop(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.world_map, (0, 0))
        self.screen.blit(self.button_image, self.button_rect)
        for c in self.destinations:
            self.screen.blit(self.city_marker,(c[0] - self.city_marker.get_rect().w / 2, c[1] - self.city_marker.get_rect().h + 9))
        if self.solving:
            self.solve_next()
        if self.curr_perm:
            pygame.draw.polygon(self.screen, 'black', self.curr_perm, width=2)
        if self.shortest_permutation:
            pygame.draw.polygon(self.screen, 'red', self.shortest_permutation, width=3)
        pygame.display.flip()
        #self.clock.tick(60)

    def reset(self):
        self.curr_perm = None
        self.solving = False
        self.shortest_distance = float("inf")
        self.shortest_permutation = None
        self.perms = permutations(self.destinations)

    def solve_next(self):
        self.curr_perm = next(self.perms, None)
        if self.curr_perm:
            distance = sum(math.dist(self.curr_perm[i - 1], self.curr_perm[i]) for i in range(len(self.curr_perm)))
            if distance < self.shortest_distance:
                self.shortest_distance = distance
                self.shortest_permutation = self.curr_perm

    def handle_click(self, pos):
        if self.button_rect.collidepoint(pos):
            self.reset()
            self.solving = True
        else:
            self.destinations.append(pos)
            self.reset()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1920, 984), pygame.FULLSCREEN)
    pygame.display.set_caption("Travelling Salesperson Animation")
    solver = TSPSolver(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                solver.handle_click(event.pos)
        solver.event_loop()


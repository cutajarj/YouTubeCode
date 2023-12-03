import random

import pygame
import math
from gatooling import generate_new_population, generate_random_paths, total_distance, choose_best, choose_worst, choose_random

from scipy.interpolate import interp1d

size = (1920, 984)
line_colour = (251, 113, 113)


class TSPSolverGA:
    def __init__(self, screen, evolutions, all_coords, generation):
        self.screen = screen
        self.evolutions = evolutions
        self.arrow_right = pygame.image.load('resouces/redArrowRight.png')
        self.arrow_right_rect = self.arrow_right.get_rect().move((180, 800))
        self.arrow_left = pygame.image.load('resouces/redArrowLeft.png')
        self.arrow_left_rect = self.arrow_left.get_rect().move((50, 800))
        self.world_map = pygame.image.load('resouces/world-map-custom.png')
        self.plane_img_red = pygame.image.load('resouces/privateJetRed.png')
        self.plane_img_green = pygame.image.load('resouces/privateJetGreen.png')
        self.plane_img_yellow = pygame.image.load('resouces/privateJetYellow.png')
        self.marker = pygame.image.load('resouces/locationMarker.png')
        self.city_marker = pygame.transform.scale(self.marker, (34, 60))
        self.plane_legend = pygame.transform.scale(self.plane_img_red, (50, 32))

        self.all_coords = all_coords
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)
        self.generation_label = pygame.font.Font(None, 30).render('Generation', True, (0, 0, 0))
        self.reset(generation)

    def get_current_generation(self):
        return self.current_generation

    def reset(self, generation):
        self.speed = 1
        self.heading_distance = 30
        self.current_generation = generation
        self.generation_count = self.font.render(f'{self.current_generation}', True, (0, 0, 0))
        self.points_in_paths = []
        self.interpolationFs = []
        self.max_distances = []
        self.all_distances = []
        self.travel_along_path = []
        self.travel_head_along_path = []
        self.shift = [(random.randint(-3, 3), random.randint(-2, 2)) for _ in self.evolutions[generation]]

        display_iteration = self.evolutions[generation]
        paths_to_show = (choose_best(all_points, display_iteration, 1) +
                       choose_random(display_iteration, 300) +
                       choose_worst(all_points, display_iteration, 1))
        for path in paths_to_show:
            current_coords = []
            for path_i in path:
                current_coords.append(self.all_coords[path_i])
            self.points_in_paths.append(current_coords)

            coordinates_x, coordinates_y = zip(*current_coords)

            total_coords = len(current_coords)
            distances = [0]
            for c in range(total_coords):
                distances.append(
                    distances[c] +
                    math.dist((coordinates_x[c], coordinates_y[c]),
                              (coordinates_x[(c + 1) % total_coords], coordinates_y[(c + 1) % total_coords]))
                )
            self.max_distances.append(int(distances[len(distances) - 1]))
            self.all_distances.append(distances)
            x_interp = interp1d(distances, coordinates_x + coordinates_x[:1])
            y_interp = interp1d(distances, coordinates_y + coordinates_y[:1])
            self.interpolationFs.append((x_interp, y_interp))
            self.travel_along_path.append(0)
            self.travel_head_along_path.append(self.heading_distance)
        self.shortest_p = self.max_distances.index(min(self.max_distances))

    def get_compass_angle(self, pt_a, pt_b):
        dx, dy = pt_b[0] - pt_a[0], pt_b[1] - pt_a[1]
        return (math.degrees(math.atan2(dy, dx)) + 90) % 360

    def event_loop(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.world_map, (0, 0))
        self.screen.blit(self.arrow_left, self.arrow_left_rect)
        self.screen.blit(self.generation_count, (123, 810))
        self.screen.blit(self.generation_label, (90, 790))
        self.screen.blit(self.arrow_right, self.arrow_right_rect)
        self.speed = min(self.speed + 0.01, 8)
        self.screen.blit(self.plane_legend, (50, 870))

        for c in self.all_coords:
            self.screen.blit(self.city_marker, (c[0] - self.city_marker.get_rect().w / 2, c[1] - self.city_marker.get_rect().h + 9))
        shortest_distances = self.all_distances[self.shortest_p]
        draw_up_to = next((i for i in range(len(shortest_distances)) if shortest_distances[i] > self.travel_along_path[self.shortest_p]), len(shortest_distances) - 1)
        for line_i in range(draw_up_to - 1):
            pygame.draw.line(self.screen, line_colour, self.points_in_paths[self.shortest_p][line_i], self.points_in_paths[self.shortest_p][line_i + 1], width=3)

        for p in range(len(self.travel_along_path)):
            if p != self.shortest_p:
                self.draw_plane(p)

        self.draw_plane(self.shortest_p)
        fast_plane_dist = self.font.render(f'{int(self.travel_along_path[self.shortest_p])}', True, (0, 0, 0))
        self.screen.blit(fast_plane_dist, (120, 870))
        pygame.display.flip()

        self.clock.tick(60)

    def draw_plane(self, p):
        x_interp, y_interp = self.interpolationFs[p]
        xy = x_interp(self.travel_along_path[p] % self.max_distances[p]), y_interp(self.travel_along_path[p] % self.max_distances[p])
        xy_heading = x_interp(self.travel_head_along_path[p]), y_interp(self.travel_head_along_path[p])

        if self.travel_along_path[p] < self.max_distances[p]:
            current_distances = self.all_distances[p]
            if p == self.shortest_p:
                last_point = next((i for i in range(len(current_distances)) if current_distances[i] > self.travel_along_path[p]), len(current_distances))
                pygame.draw.line(self.screen, line_colour, self.points_in_paths[p][last_point - 1], (int(xy[0]), int(xy[1])), width=3)
            self.travel_along_path[p] += self.speed
            self.travel_head_along_path[p] += self.speed
            self.travel_head_along_path[p] %= self.max_distances[p]
            if p == self.shortest_p:
                plane_to_draw = self.plane_img_red
            else:
                plane_to_draw = self.plane_img_yellow
        else:
            if p == self.shortest_p:
                pygame.draw.line(self.screen, line_colour, self.points_in_paths[self.shortest_p][-1], self.points_in_paths[self.shortest_p][0], width=3)
            plane_to_draw = self.plane_img_green

        rotated_plane = pygame.transform.rotate(plane_to_draw, -int(self.get_compass_angle(xy, xy_heading)))
        shifted_xy = (xy[0] + self.shift[p][0], xy[1] + self.shift[p][1])
        new_rect = rotated_plane.get_rect(center=plane_to_draw.get_rect(center=shifted_xy).center)
        self.screen.blit(rotated_plane, new_rect)

    def handle_click(self, pos, limit):
        if self.arrow_left_rect.collidepoint(pos) and solver.get_current_generation() > 0:
            self.reset(solver.get_current_generation() - 1)

        elif self.arrow_right_rect.collidepoint(pos) and solver.get_current_generation() < limit:
            self.reset(solver.get_current_generation() + 1)


if __name__ == '__main__':
    running = True
    total_iterations = 100
    evolvedIterations = []
    all_points = [(978, 359), (196, 203), (407, 292), (213, 384), (417, 589), (486, 774), (871, 470), (1194, 764), (1041, 697), (1333, 197), (1072, 258), (1524, 382), (1276, 364), (1207, 496), (1712, 811), (1837, 670), (1647, 636), (1402, 518), (1569, 640), (1770, 165), (844, 340)]

    evolvedIterations.append(generate_random_paths(len(all_points)))
    for _ in range(total_iterations):
        evolvedIterations.append(generate_new_population(all_points, evolvedIterations[-1]))

    for p in range(total_iterations):
        population = evolvedIterations[p]
        minimum = math.inf
        for path in population:
            minimum = min(minimum, total_distance(all_points, path))
        print(minimum)

    pygame.init()
    canvas = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption("Travelling Salesperson Animation")
    solver = TSPSolverGA(canvas, evolvedIterations, all_points, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                solver.handle_click(event.pos, total_iterations)
        solver.event_loop()

    pygame.quit()


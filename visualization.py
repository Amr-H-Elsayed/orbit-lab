import pygame

def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Orbital Lab")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((5, 8, 20))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
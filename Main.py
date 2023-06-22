import pygame
from Quick_sort_Animetion import QuickSort
from A_start_visivalization import PathFind


pygame.init()
WIDTH = 900
screen = pygame.display.set_mode([WIDTH, WIDTH])
clock = pygame.time.Clock()



def main():
    Animation_sort = QuickSort(screen=screen, width=WIDTH, height=WIDTH)
    Path_find = PathFind(screen=screen, rows=30, width=WIDTH)
    run = True

    select = "Q"
    while(run):
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if select == "P":
                Path_find.mouseKeyEvents(event=event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Animation_sort.pause = not Animation_sort.pause
                if event.key == pygame.K_p:
                    select = "P"
                if event.key == pygame.K_q:
                    select = "Q"
                if select == "Q" and event.key == pygame.K_r:
                    Animation_sort.reset() 


        #selcting the algorithm
        if select == "P":
            Path_find.draw_grids()
            Path_find.spots.draw_spots()
            Path_find.drawPath()
        else:
            Animation_sort.draw()


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
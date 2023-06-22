import pygame
import random
import numpy as np

pygame.init()
WIDTH = 1500
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

class QuickSort:
    
    def __init__(self, screen, width, height):
        self.size = width
        self.stack = [0]*width
        self.stack[1] = width - 1
        self.top = 1
        self.Arr = self.getArray()
        self.screen = screen
        self.width = width
        self.height = height
        self.pause = False


    def getArray(self):
        arr = np.arange(self.size)
        random.shuffle(arr)
        # arr[::-1].sort()  #decending
        arr2 = np.arange(self.size)
        return np.transpose((arr, arr2))


    def partition(self, arr,low,high):
        i = ( low - 1 )
        x = arr[high]
    
        for j in range(low , high):
            if   arr[j] <= x:
                i = i+1
                arr[i],arr[j] = arr[j],arr[i]
    
        arr[i+1],arr[high] = arr[high],arr[i+1]
        return (i+1)
        

    def Devide(self, arr):
        if(self.top) < 0:
            return 0

        h = self.stack[self.top]
        self.top = self.top - 1
        l = self.stack[self.top]
        self.top = self.top - 1

        p = self.partition(arr, l, h )
        pygame.draw.line(self.screen, (255, 0, 0), (p, 0), (p, self.height), 2)
            
        if p-1 > l:
            self.top = self.top + 1
            self.stack[self.top] = l
            self.top = self.top + 1
            self.stack[self.top] = p - 1

        if p+1 < h:
            self.top = self.top + 1
            self.stack[self.top] = p + 1
            self.top = self.top + 1
            self.stack[self.top] = h

    def draw(self):
        for cod, hig in self.Arr:
            pygame.draw.line(self.screen, (50, 50, 150), (cod, self.height), (cod, self.height-(hig/self.width)*self.height))

        if not self.pause:
            self.Devide(self.Arr[:,0])

    def reset(self):
        self.stack = [0]*self.width
        self.stack[1] = self.width - 1
        self.top = 1
        self.Arr = self.getArray()

        


def main():
    Animation_sort = QuickSort(screen, WIDTH, HEIGHT)
    run = True
    while(run):
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Animation_sort.pause = not Animation_sort.pause
        
        Animation_sort.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# main()
import pygame 
  
pygame.init() 
white = (255, 255, 255) 
X = 800
Y = 600
display_surface = pygame.display.set_mode((X, Y )) 
pygame.display.set_caption('Image') 
image = pygame.image.load(r'C:\Users\Bruno\Documents\7° SEMESTRE\Linguagens Formais e Autômatos - Segunda\Checkers\Test_Image\damas 800x600.jpg') 
while True : 
 
    display_surface.fill(white) 
  
    display_surface.blit(image, (0, 0)) 
    
    for event in pygame.event.get() : 
      
      pygame.display.update()
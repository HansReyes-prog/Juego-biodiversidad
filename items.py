import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animacion_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0 = monedas, 1 = posiones
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, posicion_panralla ,personaje):
        # reposicionar basado en el lugar de la camara o pantalla
        self.rect.x += posicion_panralla[0]
        self.rect.y += posicion_panralla[1]

        #comprobar la colisión entre el personaje y los items
        if self.rect.colliderect(personaje.forma):
            #monedas
            if self.item_type == 0:
                personaje.score +=1
            #posiones
            elif self.item_type == 1:
                personaje.energia +=50
                if personaje.energia > 100:
                    personaje.energia = 100
            self.kill()


        cooldown_animacion = 150
        self.image = self.animacion_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index  >= len(self.animacion_list):
            self.frame_index = 0


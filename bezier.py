import pygame
  
WHITE   = (255, 255, 255)
GREY   = (100, 100, 100)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 255, 255)
YELLOW  = (255, 255, 0)

FPS = 60
eps = 10
sim_freq = 0.5

def lerp(p1, p2, t):
    return (1-t)*p1 + t*p2

def main():

    points = []

    m_pressed = False
    dragging = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False     

        m_btn_vec = pygame.mouse.get_pressed()
        m_pos = pygame.Vector2(pygame.mouse.get_pos())

        m_pressed_prev_frame = m_pressed
        m_pressed = any(m_btn_vec)
        
        if not dragging:
            marked_point = None

        for p in points:
            if (p-m_pos).magnitude() < eps: # hovering over point
                marked_point = p
                break

        if m_btn_vec[0]:
            if marked_point is None and m_pressed and not m_pressed_prev_frame: # left click
                points.append(m_pos)
            else:
                idx = points.index(marked_point)
                points[idx] = m_pos
                marked_point = m_pos
                dragging = True
        else:
            dragging = False
            if m_btn_vec[2] and marked_point is not None: # right click
                idx = points.index(marked_point)
                del points[idx]

        #clear the screen
        screen.fill(BLACK)

        bezier_points = []
        for t_step in range(int(FPS/sim_freq)):
            t = t_step / (FPS//sim_freq-1)
            lerp_points = points
            for n in range(len(points)-1):
                new_lerp_points = []
                for i in range(1,len(lerp_points)):
                    p1, p2 = lerp_points[i-1], lerp_points[i] 
                    lerp_p = lerp(p1,p2,t)
                    new_lerp_points.append(lerp_p)
                lerp_points = new_lerp_points
            bezier_points = bezier_points + lerp_points

        for p in points:
            if p != marked_point:
                pygame.draw.circle(screen, RED, p, 5, 2)
            else:
                pygame.draw.circle(screen, GREEN, p, 5, 2)
        
        if len(points) > 1:
            pygame.draw.lines(screen, GREY, False, points, 2)
        
        if len(bezier_points) > 1:
            pygame.draw.lines(screen, RED, False, bezier_points, 5)
        
        # flip() updates the screen to make our changes visible
        pygame.display.flip()
        
        # maintain framerate
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    screen_size = (600, 600)
    
    # create a window
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    pygame.display.set_caption("pygame Test")
    
    # clock is used to set a max fps
    clock = pygame.time.Clock()  
    
    main()
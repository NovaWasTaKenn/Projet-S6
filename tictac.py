import pygame


def drawBoard():
    pygame.draw.rect(screen, "black", pygame.Rect(240, 60, 5, 620))
    pygame.draw.rect(screen, "black", pygame.Rect(480, 60, 5, 620))
    pygame.draw.rect(screen, "black", pygame.Rect(60, 240, 620, 5))
    pygame.draw.rect(screen, "black", pygame.Rect(60, 480, 620, 5))


def drawTic(pos, turn):
    if turn:
        pygame.draw.circle(screen, "blue", pos, 70)
    else:
        pygame.draw.circle(screen, "red", pos, 70)
    pygame.display.flip()


def action(zone):
    if board[zone-1] == 0:
        global turn
        drawTic(center[zone], turn)
        board[zone-1] = 2 if zone else 1
        turn = not turn


pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True

# Game variables
turn = False
center = {1: (120, 120), 2: (360, 120), 3: (600, 120), 4: (120, 360),
          5: (360, 360), 6: (600, 360), 7: (120, 600), 8: (360, 600), 9: (600, 600)}
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# fill the screen with a color to wipe away anything from last frame
screen.fill("white")
drawBoard()
pygame.display.flip()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < 240 and mouse_pos[1] < 240:
                action(1)
            elif mouse_pos[0] > 240 and mouse_pos[0] < 480 and mouse_pos[1] < 240:
                action(2)
            elif mouse_pos[0] > 480 and mouse_pos[0] and mouse_pos[1] < 240:
                action(3)
            elif mouse_pos[0] < 240 and mouse_pos[1] > 240 and mouse_pos[1] < 480:
                action(4)
            elif mouse_pos[0] > 240 and mouse_pos[0] < 480 and mouse_pos[1] > 240 and mouse_pos[1] < 480:
                action(5)
            elif mouse_pos[0] > 480 and mouse_pos[0] and mouse_pos[1] > 240 and mouse_pos[1] < 480:
                action(6)
            elif mouse_pos[0] < 240 and mouse_pos[1] > 480:
                action(7)
            elif mouse_pos[0] > 240 and mouse_pos[0] < 480 and mouse_pos[1] > 480 and mouse_pos[1]:
                action(8)
            elif mouse_pos[0] > 480 and mouse_pos[0] and mouse_pos[1] > 480:
                action(9)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


def alphaBetaSearch(state):
    v = maxValue(state, float('-inf'), float('inf'))
    return actions(v)


def maxValue(state, alpha, beta):
    if finParti(state):
        return utility(state)
    v = float('-inf')
    for a in actions(state):
        v = max(v, minValue(result(state, a), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def minValue(state, alpha, beta):
    if finParti(state):
        return utility(state)
    v = float('inf')
    for a in actions(state):
        v = max(v, maxValue(result(state, a), alpha, beta))
        if v <= alpha:
            return v
        beta = max(beta, v)
    return v


def finParti(state):
    for i in range(0, 3):
        if board[0+i*3] == board[1+i*3] and board[1+i*3] == board[2+i*3] and board[0+i*3] == board[2+i*3]:
            pass
        elif board[0+i] == board[3+i] and board[6+i] == board[3+i] and board[0+i] == board[6+i]:
            pass
    if board[0] == board[4] and board[4] == board[8] and board[0] == board[8]:
        pass
    elif board[2] == board[4] and board[4] == board[6] and board[2] == board[6]:
        pass


def result(state):
    pass


def utility(state):
    pass


def actions(state):
    pass

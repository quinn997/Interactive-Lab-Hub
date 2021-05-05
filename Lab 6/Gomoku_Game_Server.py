import pygame
import random
import time
import sys
import paho.mqtt.client as mqtt
import uuid


player_number = 0
current_position = (400, 400)
play_here = 0

PLAYER1 = True
# Subscribe Gomoku game
topic = 'IDD/Gomoku'

# Following codes are using the example in reader.py
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)
def on_message(cleint, userdata, msg):
    print(f"Game: {msg.topic} Player_Input: {msg.payload.decode('UTF-8')}")
    player_input = msg.payload.decode('UTF-8').split()
    position_x = int(player_input[0])
    position_y = int(player_input[1])
    global current_position
    global play_here
    global player_number
    current_position = (position_x, position_y)
    play_here = int(player_input[2])
    player_number = int(player_input[3])

    
# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)


pygame.init()
screen = pygame.display.set_mode((800, 800), 0, 32)
bg = pygame.image.load("board_background.jpg")
pygame.display.set_caption("Gomoku (Five in a Row)")
font = pygame.font.Font("C:\Windows\Fonts\BRADHITC.TTF", 40)
w_success = font.render("Player 1(White) Wins!", True, (255, 255, 255))
b_success = font.render("Player 2(Black) Wins!", True, (0, 0, 0))

USER_1 = 1
USER_2 = 2
PLAY = True  # True: White   False：Black
gameover = False


# Check piece status： 0：available  1：white 2：black
list_board_status = [[] for i in range(16)]
for i in range(0, 16):
    for j in range(0, 16):
        list_board_status[i].append(0)

# Piece Coordinates
list_board_pos = [[] for i in range(16)]
for i in range(0, 15):
    posY = i * 40 + 120
    for j in range(0, 15):
        posX = j * 40 + 120
        list_board_pos[i].append((posX, posY))

def draw_board():
    screen.blit(bg, (0, 0))
    lineColor = (0, 0, 0)
    borderWidth = 4
    lineWidth = 2
    # startP = 120
    # endP = 680
    # Boundary
    pygame.draw.line(screen, lineColor, (120, 120), (680, 120), borderWidth)  # Top
    pygame.draw.line(screen, lineColor, (120, 680), (680, 680), borderWidth)  # Bottom
    pygame.draw.line(screen, lineColor, (120, 120), (120, 680), borderWidth)  # Left
    pygame.draw.line(screen, lineColor, (680, 120), (680, 680), borderWidth)  # Right
    # Draw the board
    for i in range(1, 14):
        y = 120 + i * 40
        x = 120 + i * 40
        startP_row = (120, y)
        endP_row = (680, y)
        startP_col = (x, 120)
        endP_col = (x, 680)
        pygame.draw.line(screen, lineColor, startP_row, endP_row, lineWidth)  # horizontal lines
        pygame.draw.line(screen, lineColor, startP_col, endP_col, lineWidth)  # vertical lines
    
    # Draw the five points (400, 400) (240, 240) (240, 560) (560, 240) (560, 560)
    pygame.draw.circle(screen, lineColor, (400, 400), 4, 0)
    pygame.draw.circle(screen, lineColor, (240, 240), 4, 0)
    pygame.draw.circle(screen, lineColor, (240, 560), 4, 0)
    pygame.draw.circle(screen, lineColor, (560, 240), 4, 0)
    pygame.draw.circle(screen, lineColor, (560, 560), 4, 0)


class DrawChess:
    def __init__(self, pos=None, chess=None):
        self.pos = pos
        self.chess = chess
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        # Check piece status： 0：available  1：white 2：black
        if self.chess == 1:
            self.draw_white()
        elif self.chess == 2:
            self.draw_black()
        else:
            pass

    def draw_white(self):
        pygame.draw.circle(screen, self.white, self.pos, 20, 0)

    def draw_black(self):
        pygame.draw.circle(screen, self.black, self.pos, 20, 0)
        
class DrawCurrentLocation:
    def __init__(self, pos=None):
        self.pos = pos
        self.blue = (51, 255, 255) 
        self.circle_radius = 20
        self.border_width = 5
        self.draw_circle()

    def draw_circle(self):
        pygame.draw.circle(screen, self.blue, self.pos, self.circle_radius, self.border_width)       

class Judge:
    def __init__(self, list_status=None, play=None, chessindex=None):
        self.list_status = list_status  # board status
        self.PLAY = play  
        self.indexX, self.indexY = chessindex  # current piece location
        self.chessNum = 1  # number of pieces in a row
        self.searchAll = False  # check if searched all
        self.judge = False
        if self.PLAY:  # current player
            self.role = USER_1
        else:
            self.role = USER_2
        self.main()

    def main(self):
        moveY = self.indexY
        moveX = self.indexX
        direction = True  
        # 5 in a horizontal row
        if not self.searchAll:
            while moveY in range(0, 16):
                if direction:
                    moveY += 1
                else:
                    moveY -= 1
                if self.list_status[self.indexX][moveY] == self.role:
                    self.chessNum += 1
                else:
                   
                    if direction is False:
                        if self.chessNum < 5:
                            self.chessNum = 1  
                            direction = True
                            moveY = self.indexY
                            moveX = self.indexX
                            break
                        else:
                            pass
                    
                    direction = False
                    moveY = self.indexY

                if self.chessNum >= 5:
                    self.judge = True
                    self.searchAll = True
                    break
                else:
                    pass
        # 5 in a vertical row
        if not self.searchAll:
            while moveX in range(0, 16):
                if direction:
                    moveX += 1
                else:
                    moveX -= 1

                if self.list_status[moveX][self.indexY] == self.role:
                    self.chessNum += 1
                else:
                    
                    if direction is False:
                        if self.chessNum < 5:
                            self.chessNum = 1  
                            direction = True
                            moveY = self.indexY
                            moveX = self.indexX
                            break
                        else:
                            pass
                    
                    direction = False
                    moveX = self.indexX

                if self.chessNum >= 5:
                    self.judge = True
                    self.searchAll = True
                    break
                else:
                    pass
        # 5 in a row (top left to bottom right)
        if not self.searchAll:
            while moveX in range(0, 16) and moveY in range(0, 16):
                if direction:
                    moveX += 1
                    moveY += 1
                else:
                    moveX -= 1
                    moveY -= 1

                if self.list_status[moveX][moveY] == self.role:
                    self.chessNum += 1
                else:
                    
                    if direction is False:
                        if self.chessNum < 5:
                            self.chessNum = 1  
                            direction = True
                            moveY = self.indexY
                            moveX = self.indexX
                            break
                        else:
                            pass
                    
                    direction = False
                    moveX = self.indexX
                    moveY = self.indexY

                if self.chessNum >= 5:
                    self.judge = True
                    self.searchAll = True
                    break
                else:
                    pass
        # # 5 in a row (top right to bottom left)
        if not self.searchAll:
            while moveX in range(0, 16) and moveY in range(0, 16):
                if direction:
                    moveX += 1
                    moveY -= 1
                else:
                    moveX -= 1
                    moveY += 1

                if self.list_status[moveX][moveY] == self.role:
                    self.chessNum += 1
                else:
                    
                    if direction is False:
                        if self.chessNum < 5:
                            self.chessNum = 1  
                            direction = True
                            moveY = self.indexY
                            moveX = self.indexX
                            break
                        else:
                            pass
                    
                    direction = False
                    moveX = self.indexX
                    moveY = self.indexY

                if self.chessNum >= 5:
                    self.judge = True
                    self.searchAll = True
                    break
                else:
                    pass


# draw a board first to aviod black screen
draw_board()

last_position = (0, 0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        else:
            if play_here:
                draw_board()
                for i in range(15):
                    try:
                        index = (i, list_board_pos[i].index(current_position))
                        break
                    except ValueError:
                        pass
                # player 1 and player 2 switch
                if list_board_status[index[0]][index[1]] == 0:  # only 0 is available
                    if player_number%2 == 1 and PLAYER1:
                        list_board_status[index[0]][index[1]] = USER_1
                        judge = Judge(list_board_status, PLAYER1, (index[0], index[1]))
                        if judge.judge:
                            print("Player 1(White) Wins!")
                            screen.blit(w_success, (215, 40))
                            gameover = True
                        else:
                            pass
                        PLAYER1 = False    
                    elif player_number%2 == 0 and not PLAYER1:
                        list_board_status[index[0]][index[1]] = USER_2
                        judge = Judge(list_board_status, PLAYER1, (index[0], index[1]))
                        if judge.judge:
                            print("Player 2(Black) Wins!")
                            screen.blit(b_success, (215, 40))
                            gameover = True
                        else:
                            pass
                        PLAYER1 = True 
                else:
                    pass

                for i in range(15):
                    for j in range(15):
                        if list_board_status[i][j] == USER_1:
                            DrawChess(list_board_pos[i][j], USER_1)
                        elif list_board_status[i][j] == USER_2:
                            DrawChess(list_board_pos[i][j], USER_2)
                        else:
                            pass
                pygame.display.update()
          
            else:
                if player_number%2 == 1 and PLAYER1:
                    if current_position[0] in range(120, 681) and current_position[1] in range(120, 681) and last_position != current_position:
                        draw_board()
                        DrawCurrentLocation(current_position)
                        last_position = current_position
                        # Draw pieces
                    for i in range(15):
                        for j in range(15):
                            if list_board_status[i][j] == USER_1:
                                DrawChess(list_board_pos[i][j], USER_1)
                            elif list_board_status[i][j] == USER_2:
                                DrawChess(list_board_pos[i][j], USER_2)
                            else:
                                pass
                    pygame.display.update()
                elif player_number%2 == 0 and not PLAYER1:
                    if current_position[0] in range(120, 681) and current_position[1] in range(120, 681) and last_position != current_position:
                        draw_board()
                        DrawCurrentLocation(current_position)
                        last_position = current_position
                        # Draw pieces
                    for i in range(15):
                        for j in range(15):
                            if list_board_status[i][j] == USER_1:
                                DrawChess(list_board_pos[i][j], USER_1)
                            elif list_board_status[i][j] == USER_2:
                                DrawChess(list_board_pos[i][j], USER_2)
                            else:
                                pass
                    pygame.display.update()
    pygame.display.update()
    if gameover:
        time.sleep(5)
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    client.loop()

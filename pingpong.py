import pygame
from random import random
from pygame.constants import K_UP, K_DOWN

# Initialize Pygame and the mixer for sound
pygame.mixer.init()
pygame.init()

# Load the game over sound
gameOverSound = pygame.mixer.Sound('GameOver.mp3')

# Set up the window dimensions and other constants
WIDTH, HEIGHT = 600, 400
WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pingpong - By Tushar Mahat")  # Set the window title
BGCOLOR = (255, 255, 255)  # Background color
FPS = 60  # Frames per second
LOOP = True  # Game loop control variable

BLACK = (0, 0, 0)  # Colors for drawing shapes
BARLENGTH = 100
BARWIDTH = 10
BALLRAD = 10

# Initial positions and velocities of game elements
pcPaddleY = HEIGHT / 3
playerPaddleY = HEIGHT / 3

ballX = WIDTH / 2
ballY = HEIGHT / 2
x, y = 2, 2
isGameStopped = True
isGameOver = False

pcScore = 0
playerScore = 0

# Function to display the popup message box for game over
def showPopUp(winner):
    global LOOP
    gameOverSound.play()

    font = pygame.font.SysFont("monospace", 20)
    text_surface = font.render(f"{winner} won! Play again? (Y)es or (N)o", True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LOOP = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    resetScore()
                    return True
                elif event.key == pygame.K_n:
                    LOOP = False
                    return False
        
        WINDOWS.blit(text_surface, text_rect)
        pygame.display.flip()

# Function to reset scores
def resetScore():
    global pcScore, playerScore
    pcScore, playerScore = 0, 0

# Main update function for the game
def update():
    global isGameStopped, isGameOver
    checkWinner()
    draw()
    if not isGameStopped:
        movePosition()
    if abs(WIDTH - ballX) < BARWIDTH - BALLRAD / 2 or ballX < BARWIDTH - BALLRAD / 2:
        resetBall()
    checkWinner()
    if isGameStopped and not isGameOver:  
        showInstruction()
    updateScore()

# Function to draw game elements on the window
def draw():
    WINDOWS.fill(BGCOLOR)
    midline = pygame.draw.rect(WINDOWS, BLACK, (WIDTH / 2, 0, BARWIDTH / 4, HEIGHT))
    pcpaddle = pygame.draw.rect(WINDOWS, BLACK, (0, pcPaddleY, BARWIDTH, BARLENGTH))
    playerPaddle = pygame.draw.rect(WINDOWS, BLACK, (WIDTH - BARWIDTH, playerPaddleY, BARWIDTH, BARLENGTH))
    ball = pygame.draw.circle(WINDOWS, BLACK, (ballX, ballY), BALLRAD)

    # Draw labels for PC and player scores
    myfont = pygame.font.SysFont("monospace", 20)
    pc_label = myfont.render("PC", 1, BLACK)
    player_label = myfont.render("You", 1, BLACK)

    WINDOWS.blit(pc_label, (10, 0))  
    WINDOWS.blit(player_label, (WIDTH - 40, 0)) 

# Function to update and display scores
def updateScore():
    myfont = pygame.font.SysFont("monospace", 16)
    score = str(pcScore) + " " + str(playerScore)
    scoretext = myfont.render(score, 1, (0, 0, 0))
    WINDOWS.blit(scoretext, (WIDTH / 2 - len(score) * 5, 0))

# Function to show game instructions
def showInstruction():
    myfont = pygame.font.SysFont("monospace", 16)
    ins_start = "Press Space To Start"
    ins_move = "Use Up/Down Arrow Keys to Move"
    instext_start = myfont.render(ins_start, 1, BLACK)
    instext_move = myfont.render(ins_move, 1, BLACK)

    WINDOWS.blit(instext_start, (WIDTH / 2 - len(ins_start) * 5, HEIGHT / 2 + BALLRAD))
    WINDOWS.blit(instext_move, (WIDTH / 2 - len(ins_move) * 5, HEIGHT / 2 + BALLRAD + 20))

# Function to move game elements
def movePosition():
    global ballX, ballY
    ballX += x
    ballY += y
    bounceBallFromSides()
    bounceBallFromTopBottom()
    changeScore()

# Function to generate random values for ball movement
def generateRandomValues():
    global x, y
    randx = random()
    if randx < 0.5:
        x *= -1
    randy = random()
    if randy > 0.5:
        y *= -1

# Function to check for game winner
def checkWinner():
    global pcScore, playerScore, isGameOver
    if pcScore == 5:
        isGameOver=True
        if showPopUp("PC"):
            resetBall()
        else:
            LOOP = False
    if playerScore == 5:
        isGameOver=True
        if showPopUp("You"):
            resetBall()
        else:
            LOOP = False

# Function to reset ball position and game state
def resetBall():
    global ballX, ballY, isGameStopped, isGameOver, pcScore, playerScore, x, y
    isGameStopped = True
    isGameOver=False
    x, y = 2, 2
    ballX = WIDTH / 2
    ballY = HEIGHT / 2
    generateRandomValues()

# Function to change scores based on ball position
def changeScore():
    global ballX, ballY, pcScore, playerScore
    if abs(WIDTH - ballX) < BARWIDTH - BALLRAD / 2:
        pcScore += 1
    if ballX < BARWIDTH - BALLRAD / 2:
        playerScore += 1

# Function to handle ball bouncing from top and bottom
def bounceBallFromTopBottom():
    global y
    if ballY > HEIGHT:
        y *= -1
    if ballY < 0:
        y *= -1

# Function to handle ball bouncing from sides and paddle collisions
def bounceBallFromSides():
    global x, pcPaddleY, ballX, ballY
    pcPaddleY = ballY - pcPaddleY / 3
    if pcPaddleY >= HEIGHT - BARLENGTH:
        pcPaddleY = HEIGHT - BARLENGTH
    if abs(WIDTH - ballX) <= BARWIDTH:
        if ballY >= playerPaddleY and ballY <= playerPaddleY + BARLENGTH:
            x *= -1
            if ballY < playerPaddleY + playerPaddleY / 3 - BALLRAD or ballY > playerPaddleY - playerPaddleY / 3 + BARLENGTH:
                x *= 1.25
    if ballX <= BARWIDTH:
        if ballY >= pcPaddleY and ballY <= pcPaddleY + BARLENGTH:
            x *= -1
            if ballY < pcPaddleY + pcPaddleY / 3 - BALLRAD or ballY > pcPaddleY - pcPaddleY / 3 + BARLENGTH:
                x *= 1.25

# Function to process user input
def processInput():
    global pcPaddleY, playerPaddleY, isGameStopped, LOOP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            LOOP = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and isGameStopped:
                isGameStopped = False
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_UP]:
        playerPaddleY -= 10
        if playerPaddleY <= 0:
            playerPaddleY = 0
    if pressed_keys[K_DOWN]:
        playerPaddleY += 10
        if playerPaddleY >= HEIGHT - BARLENGTH:
            playerPaddleY = HEIGHT - BARLENGTH

# Function to update the display
def render():
    pygame.display.update()

# Main function to run the game loop
def main():
    clock = pygame.time.Clock()

    while LOOP:
        clock.tick(FPS)
        processInput()
        update()
        render()
    pygame.quit()

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
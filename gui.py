import pygame, chess
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
from tkinter import *
pygame.init()

SquareSide = 60
AISearchDepth = 1

RedCheck = (240, 150, 150)
White = (255,255, 250)
BlueLight = (140, 184, 210)
Green = (140, 180, 130)
#BlueDark = (91, 131, 159)
LichessLight = (240, 217, 181)
LichessDark = (181, 136, 99)

BoardColors = [(White, Green),(White,BlueLight)]
BoardColor = choice(BoardColors)

BlackKing = pygame.image.load('images/black_king.png')
BlackQueen = pygame.image.load('images/black_queen.png')
BlackRook = pygame.image.load('images/black_Rook.png')
BlackBishop = pygame.image.load('images/black_bishop.png')
BlackKnight = pygame.image.load('images/black_knight.png')
BlackPawn = pygame.image.load('images/black_pawn.png')
WhiteKing = pygame.image.load('images/white_king.png')
WhiteQueen = pygame.image.load('images/white_queen.png')
WhiteRook = pygame.image.load('images/white_Rook.png')
WhiteBishop = pygame.image.load('images/white_bishop.png')
WhiteKnight = pygame.image.load('images/white_knight.png')
WhitePawn = pygame.image.load('images/white_pawn.png')

Clock = pygame.time.Clock()
ClockTick = 15

Screen = pygame.display.set_mode((8 * SquareSide, 8 * SquareSide), pygame.RESIZABLE)
ScreenTitle = 'SWE Chess Game'



def printSomething():
    for x in range(1):
        label = Label(root, text=str("Playing"))
    label.pack()
root = Tk()
button = Button(root, text="Let's play", command=printSomething)
button.pack()
root.mainloop()
pygame.display.set_icon(pygame.image.load('images/chess_icon.png'))
pygame.display.set_caption(ScreenTitle)



def ResizeScreen(square_side_len):
    global SquareSide
    global Screen
    Screen = pygame.display.set_mode((8 * square_side_len, 8 * square_side_len), pygame.RESIZABLE)
    SquareSide = square_side_len


def PrintEmptyBoard():
    Screen.fill(BoardColor[0])
    PaintDarkSquares(BoardColor[1])




def PaintSquare(square, square_color):
    col = chess.FILES.index(square[0])
    row = 7 - chess.RANKS.index(square[1])
    pygame.draw.rect(Screen, square_color, (SquareSide * col, SquareSide * row, SquareSide, SquareSide), 0)


def PaintDarkSquares(square_color):
    for position in chess.SingleGen(chess.DarkSquares):
        PaintSquare(chess.bb2str(position), square_color)


def getSquareRect(square):
    col = chess.FILES.index(square[0])
    row = 7 - chess.RANKS.index(square[1])
    return pygame.Rect((col * SquareSide, row * SquareSide), (SquareSide, SquareSide))


def coord2str(position, color=chess.White):
    if color == chess.White:
        file_index = int(position[0] / SquareSide)
        rank_index = 7 - int(position[1] / SquareSide)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    if color == chess.Black:
        file_index = 7 - int(position[0] / SquareSide)
        rank_index = int(position[1] / SquareSide)
        return chess.FILES[file_index] + chess.RANKS[rank_index]


def PrintBoard(board, color=chess.White):
    if color == chess.White:
        PrintedBoard = board
    if color == chess.Black:
        PrintedBoard = chess.RotateBoard(board)

    PrintEmptyBoard()

    if chess.is_check(board, chess.White):
        PaintSquare(chess.bb2str(chess.getKing(PrintedBoard, chess.White)), RedCheck)
    if chess.is_check(board, chess.Black):
        PaintSquare(chess.bb2str(chess.getKing(PrintedBoard, chess.Black)), RedCheck)

    for position in chess.ColoredPieceGen(PrintedBoard, chess.King, chess.Black):
        Screen.blit(pygame.transform.scale(BlackKing, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Queen, chess.Black):
        Screen.blit(pygame.transform.scale(BlackQueen, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Rook, chess.Black):
        Screen.blit(pygame.transform.scale(BlackRook, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Bishop, chess.Black):
        Screen.blit(pygame.transform.scale(BlackBishop, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Knight, chess.Black):
        Screen.blit(pygame.transform.scale(BlackKnight, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Pawn, chess.Black):
        Screen.blit(pygame.transform.scale(BlackPawn, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.King, chess.White):
        Screen.blit(pygame.transform.scale(WhiteKing, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Queen, chess.White):
        Screen.blit(pygame.transform.scale(WhiteQueen, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Rook, chess.White):
        Screen.blit(pygame.transform.scale(WhiteRook, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Bishop, chess.White):
        Screen.blit(pygame.transform.scale(WhiteBishop, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Knight, chess.White):
        Screen.blit(pygame.transform.scale(WhiteKnight, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))
    for position in chess.ColoredPieceGen(PrintedBoard, chess.Pawn, chess.White):
        Screen.blit(pygame.transform.scale(WhitePawn, (SquareSide, SquareSide)),
                    getSquareRect(chess.bb2str(position)))

    pygame.display.flip()


def setTitle(title):
    pygame.display.set_caption(title)
    pygame.display.flip()



def MakeAIMove(game, color):
    setTitle(ScreenTitle + ' I am thinking...')
    new_game = chess.MakeMove(game, chess.getAIMove(game, AISearchDepth))
    setTitle(ScreenTitle)
    print("Let's start")
    PrintBoard(new_game.board, color)
    return new_game


def TryMove(game, attempted_move):
    for move in chess.LegalMoves(game, game.to_move):
        if move == attempted_move:
            game = chess.MakeMove(game, move)
    return game


def PlayAs(game, color):
    run = True
    ongoing = True

    try:
        while run:
            Clock.tick(ClockTick)
            PrintBoard(game.board, color)

            if chess.GameEnded(game):
                setTitle(ScreenTitle + ' - ' + chess.getOutcome(game))
                ongoing = False

            if ongoing and game.to_move == chess.OpposingColor(color):
                game = MakeAIMove(game, color)

            if chess.GameEnded(game):
                setTitle(ScreenTitle + ' - ' + chess.getOutcome(game))
                ongoing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    LeavingSquare = coord2str(event.pos, color)

                if event.type == pygame.MOUSEBUTTONUP:
                    arriving_square = coord2str(event.pos, color)

                    if ongoing and game.to_move == color:
                        move = (chess.str2bb(LeavingSquare), chess.str2bb(arriving_square))
                        game = TryMove(game, move)
                        PrintBoard(game.board, color)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing:  # H key
                        game = MakeAIMove(game, color)
                    if event.key == 117:  # U key
                        game = chess.UnmakeMove(game)
                        game = chess.UnmakeMove(game)
                        setTitle(ScreenTitle)
                        PrintBoard(game.board, color)
                        ongoing = True
                    if event.key == 99:  # C key
                        global BoardColor
                        new_colors = deepcopy(BoardColor)
                        new_colors.remove(BoardColor)
                        BoardColor = choice(new_colors)
                        PrintBoard(game.board, color)
                    if event.key == 112 or event.key == 100:  # P or D key
                        print(game.get_move_list() + '\n')
                        print('\n'.join(game.position_history))
                    if event.key == 101:  # E key
                        print('eval = ' + str(chess.evaluate_game(game) / 100))

                if event.type == pygame.VIDEORESIZE:
                    if Screen.get_height() != event.h:
                        ResizeScreen(int(event.h / 8.0))
                    elif Screen.get_width() != event.w:
                        ResizeScreen(int(event.w / 8.0))
                    PrintBoard(game.board, color)
    except:
        print(format_exc(), file=stderr)
        bug_file = open('bug_report.txt', 'a')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nPlaying as WHITE:\n\t' if color == chess.White else '\nPlaying as BLACK:\n\t')
        bug_file.write(game.getMoveList() + '\n\t')
        bug_file.write('\n\t'.join(game.position_history))
        bug_file.write('\n-----------------------------\n\n')
        bug_file.close()


def PlayAsWhite(game=chess.GamePosition()):
    return PlayAs(game, chess.White)


def PlayAsBlack(game=chess.GamePosition()):
    return PlayAs(game, chess.Black)


def PlayRandomColor(game=chess.GamePosition()):
    color = choice([chess.White, chess.Black])
    PlayAs(game, color)


# chess.verbose = True
PlayRandomColor()

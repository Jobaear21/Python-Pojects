from copy import deepcopy
from random import choice
from time import sleep, time
from tkinter import *
ColorMask = 1 << 3
White = 0 << 3
Black = 1 << 3

EndgamePieceCount = 7

PieceMask = 0b111
Empty = 0
Pawn = 1
Knight = 2
Bishop = 3
Rook = 4
Queen = 5
King = 6

PieceTypes = [Pawn, Knight, Bishop, Rook, Queen, King]
PieceValues = {Empty: 0, Pawn: 100, Knight: 300, Bishop: 300, Rook: 500, Queen: 900, King: 42000}

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']

CastleKingSideWhite = 0b1 << 0
CastleQueenSideWhite = 0b1 << 1
CastleKingSideBlack = 0b1 << 2
CastleQueenSideBlack = 0b1 << 3

FullCastlingRights = CastleKingSideWhite | CastleQueenSideWhite | CastleKingSideBlack | CastleQueenSideBlack

AllSquares = 0xFFFFFFFFFFFFFFFF
FileA = 0x0101010101010101
FileB = 0x0202020202020202
FileC = 0x0404040404040404
FileD = 0x0808080808080808
FileE = 0x1010101010101010
FileF = 0x2020202020202020
FileG = 0x4040404040404040
FileH = 0x8080808080808080
Rank1 = 0x00000000000000FF
Rank2 = 0x000000000000FF00
Rank3 = 0x0000000000FF0000
Rank4 = 0x00000000FF000000
Rank5 = 0x000000FF00000000
Rank6 = 0x0000FF0000000000
Rank7 = 0x00FF000000000000
Rank8 = 0xFF00000000000000
DiagA1toH8 = 0x8040201008040201
AntiDiagH1toA8 = 0x0102040810204080
LightSquares = 0x55AA55AA55AA55AA
DarkSquares = 0xAA55AA55AA55AA55

FileMasks = [FileA, FileB, FileC, FileD, FileE, FileF, FileG, FileH]
RankMASKS = [Rank1, Rank2, Rank3, Rank4, Rank5, Rank6, Rank7, Rank8]

InitialBoard = [White | Rook, White | Knight, White | Bishop, White | Queen, White | King, White | Bishop,
                White | Knight, White | Rook,
                White | Pawn, White | Pawn, White | Pawn, White | Pawn, White | Pawn, White | Pawn, White | Pawn,
                White | Pawn,
                Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
                Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
                Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
                Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
                Black | Pawn, Black | Pawn, Black | Pawn, Black | Pawn, Black | Pawn, Black | Pawn, Black | Pawn,
                Black | Pawn,
                Black | Rook, Black | Knight, Black | Bishop, Black | Queen, Black | King, Black | Bishop,
                Black | Knight, Black | Rook]

EmptyBoard = [Empty for _ in range(64)]

InitialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
StrokesYolo = '1k6/2b1p3/Qp4N1/4r2P/2B2q2/1R6/2Pn2K1/8 w - - 0 1'

PieceCodes = {White | King: 'K',
              White | Queen: 'Q',
              White | Rook: 'R',
              White | Bishop: 'B',
              White | Knight: 'N',
              White | Pawn: 'P',
              Black | King: 'k',
              Black | Queen: 'q',
              Black | Rook: 'r',
              Black | Bishop: 'b',
              Black | Knight: 'n',
              Black | Pawn: 'p',
              Empty: '.'}
PieceCodes.update({v: k for k, v in PieceCodes.items()})

DoubledPawnPenalty = 10
IsolatedPawnPenalty = 20
BackwardPawnPenalty = 8
PassedPawnBonus = 20
RookSemiOpenFileBonus = 10
RookOpenFileBonus = 15
RookOnSeventhBonus = 20

PawnBonus = [0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, -40, -40, 0, 0, 0,
              1, 2, 3, -10, -10, 3, 2, 1,
              2, 4, 6, 8, 8, 6, 4, 2,
              3, 6, 9, 12, 12, 9, 6, 3,
              4, 8, 12, 16, 16, 12, 8, 4,
              5, 10, 15, 20, 20, 15, 10, 5,
              0, 0, 0, 0, 0, 0, 0, 0]

KnightBonus = [-10, -30, -10, -10, -10, -10, -30, -10,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, -10, -10, -10, -10, -10, -10, -10]

BishopBonus = [-10, -10, -20, -10, -10, -20, -10, -10,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, -10, -10, -10, -10, -10, -10, -10]

KingBonus = [0, 20, 40, -20, 0, -20, 40, 20,
              -20, -20, -20, -20, -20, -20, -20, -20,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40,
              -40, -40, -40, -40, -40, -40, -40, -40]

KingEndgameBonus = [0, 10, 20, 30, 30, 20, 10, 0,
                      10, 20, 30, 40, 40, 30, 20, 10,
                      20, 30, 40, 50, 50, 40, 30, 20,
                      30, 40, 50, 60, 60, 50, 40, 30,
                      30, 40, 50, 60, 60, 50, 40, 30,
                      20, 30, 40, 50, 50, 40, 30, 20,
                      10, 20, 30, 40, 40, 30, 20, 10,
                      0, 10, 20, 30, 30, 20, 10, 0]

verbose = False


# ========== CHESS GAME ==========

class GamePosition:
    def __init__(self, FEN=''):
        self.board = InitialBoard
        self.to_move = White
        self.ep_square = 0
        self.castling_rights = FullCastlingRights
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.position_history = []
        if FEN != '':
            self.LoadFEN(FEN)
            self.position_history.append(FEN)
        else:
            self.position_history.append(InitialFEN)

        self.move_history = []

    def getMoveList(self):
        return ' '.join(self.move_history)

    def toFEN(self):
        FEN_str = ''

        for i in range(len(RANKS)):
            first = len(self.board) - 8 * (i + 1)
            empty_sqrs = 0
            for fille in range(len(FILES)):
                piece = self.board[first + fille]
                if piece & PieceMask == Empty:
                    empty_sqrs += 1
                else:
                    if empty_sqrs > 0:
                        FEN_str += '{}'.format(empty_sqrs)
                    FEN_str += '{}'.format(piece2str(piece))
                    empty_sqrs = 0
            if empty_sqrs > 0:
                FEN_str += '{}'.format(empty_sqrs)
            FEN_str += '/'
        FEN_str = FEN_str[:-1] + ' '

        if self.to_move == White:
            FEN_str += 'w '
        if self.to_move == Black:
            FEN_str += 'b '

        if self.castling_rights & CastleKingSideWhite:
            FEN_str += 'K'
        if self.castling_rights & CastleQueenSideWhite:
            FEN_str += 'Q'
        if self.castling_rights & CastleKingSideBlack:
            FEN_str += 'k'
        if self.castling_rights & CastleQueenSideBlack:
            FEN_str += 'q'
        if self.castling_rights == 0:
            FEN_str += '-'
        FEN_str += ' '

        if self.ep_square == 0:
            FEN_str += '-'
        else:
            FEN_str += bb2str(self.ep_square)

        FEN_str += ' {}'.format(self.halfmove_clock)
        FEN_str += ' {}'.format(self.fullmove_number)
        return FEN_str

    def LoadFEN(self, FEN_str):
        FEN_list = FEN_str.split(' ')

        board_str = FEN_list[0]
        rank_list = board_str.split('/')
        rank_list.reverse()
        self.board = []

        for rank in rank_list:
            rank_pieces = []
            for p in rank:
                if p.isdigit():
                    for _ in range(int(p)):
                        rank_pieces.append(Empty)
                else:
                    rank_pieces.append(str2piece(p))
            self.board.extend(rank_pieces)

        to_move_str = FEN_list[1].lower()
        if to_move_str == 'w':
            self.to_move = White
        if to_move_str == 'b':
            self.to_move = Black

        castling_rights_str = FEN_list[2]
        self.castling_rights = 0
        if castling_rights_str.find('K') >= 0:
            self.castling_rights |= CastleKingSideWhite
        if castling_rights_str.find('Q') >= 0:
            self.castling_rights |= CastleQueenSideWhite
        if castling_rights_str.find('k') >= 0:
            self.castling_rights |= CastleKingSideBlack
        if castling_rights_str.find('q') >= 0:
            self.castling_rights |= CastleQueenSideBlack

        ep_str = FEN_list[3]
        if ep_str == '-':
            self.ep_square = 0
        else:
            self.ep_square = str2bb(ep_str)

        self.halfmove_clock = int(FEN_list[4])
        self.fullmove_number = int(FEN_list[5])


# ================================


def getPiece(board, bitboard):
    return board[bb2index(bitboard)]


def bb2index(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            return i


def str2index(position_str):
    fille = FILES.index(position_str[0].lower())
    rank = RANKS.index(position_str[1])
    return 8 * rank + fille


def bb2str(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            fille = i % 8
            rank = int(i / 8)
            return '{}{}'.format(FILES[fille], RANKS[rank])


def str2bb(position_str):
    return 0b1 << str2index(position_str)


def move2str(move):
    return bb2str(move[0]) + bb2str(move[1])


def SingleGen(bitboard):
    for i in range(64):
        bit = 0b1 << i
        if bitboard & bit:
            yield bit


def PieceGen(board, piece_code):
    for i in range(64):
        if board[i] & PieceMask == piece_code:
            yield 0b1 << i


def ColoredPieceGen(board, piece_code, color):
    for i in range(64):
        if board[i] == piece_code | color:
            yield 0b1 << i


def OpposingColor(color):
    if color == White:
        return Black
    if color == Black:
        return White


def piece2str(piece):
    return PieceCodes[piece]


def str2piece(string):
    return PieceCodes[string]


def PrintBoard(board):
    print('')
    for i in range(len(RANKS)):
        rank_str = str(8 - i) + ' '
        first = len(board) - 8 * (i + 1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece2str(board[first + fille]))
        print(rank_str)
    print('  a b c d e f g h')


def PrintRotatedBoard(board):
    r_board = RotateBoard(board)
    print('')
    for i in range(len(RANKS)):
        rank_str = str(i + 1) + ' '
        first = len(r_board) - 8 * (i + 1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece2str(r_board[first + fille]))
        print(rank_str)
    print('  h g f e d c b a')


def printBitBoard(bitboard):
    print('')
    for rank in range(len(RANKS)):
        rank_str = str(8 - rank) + ' '
        for fille in range(len(FILES)):
            if (bitboard >> (fille + (7 - rank) * 8)) & 0b1:
                rank_str += '# '
            else:
                rank_str += '. '
        print(rank_str)
    print('  a b c d e f g h')


def lsb(bitboard):
    for i in range(64):
        bit = (0b1 << i)
        if bit & bitboard:
            return bit


def msb(bitboard):
    for i in range(64):
        bit = (0b1 << (63 - i))
        if bit & bitboard:
            return bit


def getColoredPieces(board, color):
    return list2int([(i != Empty and i & ColorMask == color) for i in board])


def EmptySquares(board):
    return list2int([i == Empty for i in board])


def OccupiedSquares(board):
    return nnot(EmptySquares(board))


def list2int(lst):
    rev_list = lst[:]
    rev_list.reverse()
    return int('0b' + ''.join(['1' if i else '0' for i in rev_list]), 2)


def nnot(bitboard):
    return ~bitboard & AllSquares


def RotateBoard(board):
    rotated_board = deepcopy(board)
    rotated_board.reverse()
    return rotated_board


def FlipBoardV(board):
    flip = [56, 57, 58, 59, 60, 61, 62, 63,
            48, 49, 50, 51, 52, 53, 54, 55,
            40, 41, 42, 43, 44, 45, 46, 47,
            32, 33, 34, 35, 36, 37, 38, 39,
            24, 25, 26, 27, 28, 29, 30, 31,
            16, 17, 18, 19, 20, 21, 22, 23,
            8, 9, 10, 11, 12, 13, 14, 15,
            0, 1, 2, 3, 4, 5, 6, 7]

    return deepcopy([board[flip[i]] for i in range(64)])


def EastOne(bitboard):
    return (bitboard << 1) & nnot(FileA)


def WestOne(bitboard):
    return (bitboard >> 1) & nnot(FileH)


def NorthOne(bitboard):
    return (bitboard << 8) & nnot(Rank1)


def SouthOne(bitboard):
    return (bitboard >> 8) & nnot(Rank8)


def NeOne(bitboard):
    return NorthOne(EastOne(bitboard))


def NwOne(bitboard):
    return NorthOne(WestOne(bitboard))


def SeOne(bitboard):
    return SouthOne(EastOne(bitboard))


def SwOne(bitboard):
    return SouthOne(WestOne(bitboard))


def MovePiece(board, move):
    new_board = deepcopy(board)
    new_board[bb2index(move[1])] = new_board[bb2index(move[0])]
    new_board[bb2index(move[0])] = Empty
    return new_board


def MakeMove(game, move):
    new_game = deepcopy(game)
    leaving_position = move[0]
    arriving_position = move[1]

    # update_clocks
    new_game.halfmove_clock += 1
    if new_game.to_move == Black:
        new_game.fullmove_number += 1

    # reset clock if capture
    if getPiece(new_game.board, arriving_position) != Empty:
        new_game.halfmove_clock = 0

    # for pawns: reset clock, removed captured ep, set new ep, promote
    if getPiece(new_game.board, leaving_position) & PieceMask == Pawn:
        new_game.halfmove_clock = 0

        if arriving_position == game.ep_square:
            new_game.board = RemoveCapturedEp(new_game)

        if IsDoublePush(leaving_position, arriving_position):
            new_game.ep_square = NewEpSquare(leaving_position)

        if arriving_position & (Rank1 | Rank8):
            new_game.board[bb2index(leaving_position)] = new_game.to_move | Queen

    # reset ep square if not updated
    if new_game.ep_square == game.ep_square:
        new_game.ep_square = 0

    # update castling rights for rook moves
    if leaving_position == str2bb('a1'):
        new_game.castling_rights = RemoveCastlingRights(new_game, CastleQueenSideWhite)
    if leaving_position == str2bb('h1'):
        new_game.castling_rights = RemoveCastlingRights(new_game, CastleKingSideWhite)
    if leaving_position == str2bb('a8'):
        new_game.castling_rights = RemoveCastlingRights(new_game, CastleQueenSideBlack)
    if leaving_position == str2bb('h8'):
        new_game.castling_rights = RemoveCastlingRights(new_game, CastleKingSideBlack)

    # castling
    if getPiece(new_game.board, leaving_position) == White | King:
        new_game.castling_rights = RemoveCastlingRights(new_game, CastleKingSideWhite | CastleQueenSideWhite)
        if leaving_position == str2bb('e1'):
            if arriving_position == str2bb('g1'):
                new_game.board = MovePiece(new_game.board, [str2bb('h1'), str2bb('f1')])
            if arriving_position == str2bb('c1'):
                new_game.board = MovePiece(new_game.board, [str2bb('a1'), str2bb('d1')])

    if getPiece(new_game.board, leaving_position) == Black | King:
        new_game.castling_rights = RemoveCastlingRights(new_game, CastleKingSideBlack | CastleQueenSideBlack)
        if leaving_position == str2bb('e8'):
            if arriving_position == str2bb('g8'):
                new_game.board = MovePiece(new_game.board, [str2bb('h8'), str2bb('f8')])
            if arriving_position == str2bb('c8'):
                new_game.board = MovePiece(new_game.board, [str2bb('a8'), str2bb('d8')])

    # update positions and next to move
    new_game.board = MovePiece(new_game.board, (leaving_position, arriving_position))
    new_game.to_move = OpposingColor(new_game.to_move)

    # update history
    new_game.move_history.append(move2str(move))
    new_game.position_history.append(new_game.toFEN())
    return new_game


def UnMakeMove(game):
    if len(game.position_history) < 2:
        return deepcopy(game)

    new_game = GamePosition(game.position_history[-2])
    new_game.move_history = deepcopy(game.move_history)[:-1]
    new_game.position_history = deepcopy(game.position_history)[:-1]
    return new_game


def getRank(rank_num):
    rank_num = int(rank_num)
    return RankMASKS[rank_num]


def getFile(file_str):
    file_str = file_str.lower()
    file_num = FILES.index(file_str)
    return FileMasks[file_num]


def getFilter(filter_str):
    if filter_str in FILES:
        return getFile(filter_str)
    if filter_str in RANKS:
        return getRank(filter_str)


# ========== Pawn ==========

def getAllPawns(board):
    return list2int([i & PieceMask == Pawn for i in board])


def getPawns(board, color):
    return list2int([i == color | Pawn for i in board])


def PawnMoves(moving_piece, game, color):
    return PawnPushes(moving_piece, game.board, color) | PawnCaptures(moving_piece, game, color)


def PawnCaptures(moving_piece, game, color):
    return PawnSimpleCaptures(moving_piece, game, color) | PawnEpCaptures(moving_piece, game, color)


def PawnPushes(moving_piece, board, color):
    return PawnSimplePushes(moving_piece, board, color) | PawnDoublePushes(moving_piece, board, color)


def PawnSimpleCaptures(attacking_piece, game, color):
    return PawnAttacks(attacking_piece, game.board, color) & getColoredPieces(game.board, OpposingColor(color))


def PawnEpCaptures(attacking_piece, game, color):
    if color == White:
        ep_squares = game.ep_square & Rank6
    if color == Black:
        ep_squares = game.ep_square & Rank3
    return PawnAttacks(attacking_piece, game.board, color) & ep_squares


def PawnAttacks(attacking_piece, board, color):
    return PawnEastAttacks(attacking_piece, board, color) | PawnWestAttacks(attacking_piece, board, color)


def PawnSimplePushes(moving_piece, board, color):
    if color == White:
        return NorthOne(moving_piece) & EmptySquares(board)
    if color == Black:
        return SouthOne(moving_piece) & EmptySquares(board)


def PawnDoublePushes(moving_piece, board, color):
    if color == White:
        return NorthOne(PawnSimplePushes(moving_piece, board, color)) & (EmptySquares(board) & Rank4)
    if color == Black:
        return SouthOne(PawnSimplePushes(moving_piece, board, color)) & (EmptySquares(board) & Rank5)


def PawnEastAttacks(attacking_piece, board, color):
    if color == White:
        return NeOne(attacking_piece & getColoredPieces(board, color))
    if color == Black:
        return SeOne(attacking_piece & getColoredPieces(board, color))


def PawnWestAttacks(attacking_piece, board, color):
    if color == White:
        return NwOne(attacking_piece & getColoredPieces(board, color))
    if color == Black:
        return SwOne(attacking_piece & getColoredPieces(board, color))


def PawnDoubleAttacks(attacking_piece, board, color):
    return PawnEastAttacks(attacking_piece, board, color) & PawnWestAttacks(attacking_piece, board, color)


def IsDoublePush(leaving_square, target_square):
    return (leaving_square & Rank2 and target_square & Rank4) or \
           (leaving_square & Rank7 and target_square & Rank5)


def NewEpSquare(leaving_square):
    if leaving_square & Rank2:
        return NorthOne(leaving_square)
    if leaving_square & Rank7:
        return SouthOne(leaving_square)


def RemoveCapturedEp(game):
    new_board = deepcopy(game.board)
    if game.ep_square & Rank3:
        new_board[bb2index(NorthOne(game.ep_square))] = Empty
    if game.ep_square & Rank6:
        new_board[bb2index(SouthOne(game.ep_square))] = Empty
    return new_board


# ========== Knight ==========

def getKnights(board, color):
    return list2int([i == color | Knight for i in board])


def KnightMoves(moving_piece, board, color):
    return KnightAttacks(moving_piece) & nnot(getColoredPieces(board, color))


def KnightAttacks(moving_piece):
    return KnightNNE(moving_piece) | \
           KnightENE(moving_piece) | \
           KnightNNW(moving_piece) | \
           KnightWNW(moving_piece) | \
           KnightSSE(moving_piece) | \
           KnightESE(moving_piece) | \
           KnightSSW(moving_piece) | \
           KnightWSW(moving_piece)


def KnightWNW(moving_piece):
    return moving_piece << 6 & nnot(FileG | FileH)


def KnightENE(moving_piece):
    return moving_piece << 10 & nnot(FileA | FileB)


def KnightNNW(moving_piece):
    return moving_piece << 15 & nnot(FileH)


def KnightNNE(moving_piece):
    return moving_piece << 17 & nnot(FileA)


def KnightESE(moving_piece):
    return moving_piece >> 6 & nnot(FileA | FileB)


def KnightWSW(moving_piece):
    return moving_piece >> 10 & nnot(FileG | FileH)


def KnightSSE(moving_piece):
    return moving_piece >> 15 & nnot(FileA)


def KnightSSW(moving_piece):
    return moving_piece >> 17 & nnot(FileH)


def KnightFill(moving_piece, n):
    fill = moving_piece
    for _ in range(n):
        fill |= KnightAttacks(fill)
    return fill


def KnightDistance(pos1, pos2):
    init_bitboard = str2bb(pos1)
    end_bitboard = str2bb(pos2)
    fill = init_bitboard
    dist = 0
    while fill & end_bitboard == 0:
        dist += 1
        fill = KnightFill(init_bitboard, dist)
    return dist


# ========== King ==========

def getKing(board, color):
    return list2int([i == color | King for i in board])


def KingMoves(moving_piece, board, color):
    return KingAttacks(moving_piece) & nnot(getColoredPieces(board, color))


def KingAttacks(moving_piece):
    king_atks = moving_piece | EastOne(moving_piece) | WestOne(moving_piece)
    king_atks |= NorthOne(king_atks) | SouthOne(king_atks)
    return king_atks & nnot(moving_piece)


def CanCastleKingSide(game, color):
    if color == White:
        return (game.castling_rights & CastleKingSideWhite) and \
               game.board[str2index('f1')] == Empty and \
               game.board[str2index('g1')] == Empty and \
               (not IsAttacked(str2bb('e1'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('f1'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('g1'), game.board, OpposingColor(color)))
    if color == Black:
        return (game.castling_rights & CastleKingSideBlack) and \
               game.board[str2index('f8')] == Empty and \
               game.board[str2index('g8')] == Empty and \
               (not IsAttacked(str2bb('e8'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('f8'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('g8'), game.board, OpposingColor(color)))


def CanCastleQueenSide(game, color):
    if color == White:
        return (game.castling_rights & CastleQueenSideWhite) and \
               game.board[str2index('b1')] == Empty and \
               game.board[str2index('c1')] == Empty and \
               game.board[str2index('d1')] == Empty and \
               (not IsAttacked(str2bb('c1'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('d1'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('e1'), game.board, OpposingColor(color)))
    if color == Black:
        return (game.castling_rights & CastleQueenSideBlack) and \
               game.board[str2index('b8')] == Empty and \
               game.board[str2index('c8')] == Empty and \
               game.board[str2index('d8')] == Empty and \
               (not IsAttacked(str2bb('c8'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('d8'), game.board, OpposingColor(color))) and \
               (not IsAttacked(str2bb('e8'), game.board, OpposingColor(color)))


def CastleKingSideMove(game):
    if game.to_move == White:
        return (str2bb('e1'), str2bb('g1'))
    if game.to_move == Black:
        return (str2bb('e8'), str2bb('g8'))


def CastleQueenSideMove(game):
    if game.to_move == White:
        return (str2bb('e1'), str2bb('c1'))
    if game.to_move == Black:
        return (str2bb('e8'), str2bb('c8'))


def RemoveCastlingRights(game, removed_rights):
    return game.castling_rights & ~removed_rights


# ========== Bishop ==========

def getBishops(board, color):
    return list2int([i == color | Bishop for i in board])


def BishopRays(moving_piece):
    return DiagonalRays(moving_piece) | AntiDiagonalRays(moving_piece)


def DiagonalRays(moving_piece):
    return NeRay(moving_piece) | SwRay(moving_piece)


def AntiDiagonalRays(moving_piece):
    return NwRay(moving_piece) | SeRay(moving_piece)


def NeRay(moving_piece):
    ray_atks = NeOne(moving_piece)
    for _ in range(6):
        ray_atks |= NeOne(ray_atks)
    return ray_atks & AllSquares


def SeRay(moving_piece):
    ray_atks = SeOne(moving_piece)
    for _ in range(6):
        ray_atks |= SeOne(ray_atks)
    return ray_atks & AllSquares


def NwRay(moving_piece):
    ray_atks = NwOne(moving_piece)
    for _ in range(6):
        ray_atks |= NwOne(ray_atks)
    return ray_atks & AllSquares


def SwRay(moving_piece):
    ray_atks = SwOne(moving_piece)
    for _ in range(6):
        ray_atks |= SwOne(ray_atks)
    return ray_atks & AllSquares


def NeAttacks(single_piece, board, color):
    blocker = lsb(NeRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return NeRay(single_piece) ^ NeRay(blocker)
    else:
        return NeRay(single_piece)


def NwAttacks(single_piece, board, color):
    blocker = lsb(NwRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return NwRay(single_piece) ^ NwRay(blocker)
    else:
        return NwRay(single_piece)


def SeAttacks(single_piece, board, color):
    blocker = msb(SeRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return SeRay(single_piece) ^ SeRay(blocker)
    else:
        return SeRay(single_piece)


def SwAttacks(single_piece, board, color):
    blocker = msb(SwRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return SwRay(single_piece) ^ SwRay(blocker)
    else:
        return SwRay(single_piece)


def DiagonalAttacks(single_piece, board, color):
    return NeAttacks(single_piece, board, color) | SwAttacks(single_piece, board, color)


def AntiDiagonalAttacks(single_piece, board, color):
    return NwAttacks(single_piece, board, color) | SeAttacks(single_piece, board, color)


def BishopAttacks(moving_piece, board, color):
    atks = 0
    for piece in SingleGen(moving_piece):
        atks |= DiagonalAttacks(piece, board, color) | AntiDiagonalAttacks(piece, board, color)
    return atks


def BishopMoves(moving_piece, board, color):
    return BishopAttacks(moving_piece, board, color) & nnot(getColoredPieces(board, color))


# ========== Rook ==========

def getRooks(board, color):
    return list2int([i == color | Rook for i in board])


def RookRays(moving_piece):
    return RankRays(moving_piece) | FileRays(moving_piece)


def RankRays(moving_piece):
    return EastRay(moving_piece) | WestRay(moving_piece)


def FileRays(moving_piece):
    return NorthRay(moving_piece) | SouthRay(moving_piece)


def EastRay(moving_piece):
    ray_atks = EastOne(moving_piece)
    for _ in range(6):
        ray_atks |= EastOne(ray_atks)
    return ray_atks & AllSquares


def WestRay(moving_piece):
    ray_atks = WestOne(moving_piece)
    for _ in range(6):
        ray_atks |= WestOne(ray_atks)
    return ray_atks & AllSquares


def NorthRay(moving_piece):
    ray_atks = NorthOne(moving_piece)
    for _ in range(6):
        ray_atks |= NorthOne(ray_atks)
    return ray_atks & AllSquares


def SouthRay(moving_piece):
    ray_atks = SouthOne(moving_piece)
    for _ in range(6):
        ray_atks |= SouthOne(ray_atks)
    return ray_atks & AllSquares


def EastAttacks(single_piece, board, color):
    blocker = lsb(EastRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return EastRay(single_piece) ^ EastRay(blocker)
    else:
        return EastRay(single_piece)


def WestAttacks(single_piece, board, color):
    blocker = msb(WestRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return WestRay(single_piece) ^ WestRay(blocker)
    else:
        return WestRay(single_piece)


def RankAttacks(single_piece, board, color):
    return EastAttacks(single_piece, board, color) | WestAttacks(single_piece, board, color)


def NorthAttacks(single_piece, board, color):
    blocker = lsb(NorthRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return NorthRay(single_piece) ^ NorthRay(blocker)
    else:
        return NorthRay(single_piece)


def SouthAttacks(single_piece, board, color):
    blocker = msb(SouthRay(single_piece) & OccupiedSquares(board))
    if blocker:
        return SouthRay(single_piece) ^ SouthRay(blocker)
    else:
        return SouthRay(single_piece)


def FileAttacks(single_piece, board, color):
    return NorthAttacks(single_piece, board, color) | SouthAttacks(single_piece, board, color)


def RookAttacks(moving_piece, board, color):
    atks = 0
    for single_piece in SingleGen(moving_piece):
        atks |= RankAttacks(single_piece, board, color) | FileAttacks(single_piece, board, color)
    return atks


def RookMoves(moving_piece, board, color):
    return RookAttacks(moving_piece, board, color) & nnot(getColoredPieces(board, color))


# ========== Queen ==========

def getQueen(board, color):
    return list2int([i == color | Queen for i in board])


def QueenRays(moving_piece):
    return RookRays(moving_piece) | BishopRays(moving_piece)


def QueenAttacks(moving_piece, board, color):
    return BishopAttacks(moving_piece, board, color) | RookAttacks(moving_piece, board, color)


def QueenMoves(moving_piece, board, color):
    return BishopMoves(moving_piece, board, color) | RookMoves(moving_piece, board, color)


def IsAttacked(target, board, attacking_color):
    return CountAttacks(target, board, attacking_color) > 0


def is_check(board, color):
    return IsAttacked(getKing(board, color), board, OpposingColor(color))


def getAttacks(moving_piece, board, color):
    piece = board[bb2index(moving_piece)]

    if piece & PieceMask == Pawn:
        return PawnAttacks(moving_piece, board, color)
    elif piece & PieceMask == Knight:
        return KnightAttacks(moving_piece)
    elif piece & PieceMask == Bishop:
        return BishopAttacks(moving_piece, board, color)
    elif piece & PieceMask == Rook:
        return RookAttacks(moving_piece, board, color)
    elif piece & PieceMask == Queen:
        return QueenAttacks(moving_piece, board, color)
    elif piece & PieceMask == King:
        return KingAttacks(moving_piece)


def getMoves(moving_piece, game, color):
    piece = game.board[bb2index(moving_piece)]

    if piece & PieceMask == Pawn:

        return PawnMoves(moving_piece, game, color)

    elif piece & PieceMask == Knight:
        return KnightMoves(moving_piece, game.board, color)
    elif piece & PieceMask == Bishop:
        return BishopMoves(moving_piece, game.board, color)
    elif piece & PieceMask == Rook:
        return RookMoves(moving_piece, game.board, color)
    elif piece & PieceMask == Queen:
        def printSomething():
            for x in range(1):
                label = Label(root, text="Playing")
            label.pack()

        root = Tk()
        button = Button(root, text="Sure move", command=printSomething)
        button.pack()
        root.mainloop()
        return QueenMoves(moving_piece, game.board, color)
    elif piece & PieceMask == King:
        return KingMoves(moving_piece, game.board, color)


def CountAttacks(target, board, attacking_color):
    attack_count = 0

    for index in range(64):
        piece = board[index]
        if piece != Empty and piece & ColorMask == attacking_color:
            pos = 0b1 << index

            if getAttacks(pos, board, attacking_color) & target:
                attack_count += 1

    return attack_count


def MaterialSum(board, color):
    material = 0
    for piece in board:
        if piece & ColorMask == color:
            material += PieceValues[piece & PieceMask]
    return material


def MaterialBalance(board):
    return MaterialSum(board, White) - MaterialSum(board, Black)


def MobilityBalance(game):
    return CountLegalMoves(game, White) - CountLegalMoves(game, Black)


def evaluate_game(game):
    if GameEnded(game):
        return EvaluateEndNode(game)
    else:
        return MaterialBalance(game.board) + PositionalBalance(game)  # + 10*MobilityBalance(game)


def EvaluateEndNode(game):
    if IsCheckmate(game, game.to_move):
        return WinScore(game.to_move)
    elif IsStalemate(game) or \
            HasInsufficientMaterial(game) or \
            Under75Move(game):
        return 0


def PositionalBalance(game):
    return PositionalBonus(game, White) - PositionalBonus(game, Black)


def PositionalBonus(game, color):
    bonus = 0

    if color == White:
        board = game.board
    elif color == Black:
        board = FlipBoardV(game.board)

    for index in range(64):
        piece = board[index]

        if piece != Empty and piece & ColorMask == color:
            piece_type = piece & PieceMask

            if piece_type == Pawn:
                bonus += PawnBonus[index]
            elif piece_type == Knight:
                bonus += KnightBonus[index]
            elif piece_type == Bishop:
                bonus += BishopBonus[index]

            elif piece_type == Rook:
                position = 0b1 << index

                if IsOpenFile(position, board):
                    bonus += RookOpenFileBonus
                elif IsSemiOpenFile(position, board):
                    bonus += RookSemiOpenFileBonus

                if position & Rank7:
                    bonus += RookOnSeventhBonus

            elif piece_type == King:
                if IsEndgame(board):
                    bonus += KingEndgameBonus[index]
                else:
                    bonus += KingBonus[index]

    return bonus


def IsEndgame(board):
    return CountPieces(OccupiedSquares(board)) <= EndgamePieceCount


def IsOpenFile(bitboard, board):
    for f in FILES:
        rank_filter = getFile(f)
        if bitboard & rank_filter:
            return CountPieces(getAllPawns(board) & rank_filter) == 0


def IsSemiOpenFile(bitboard, board):
    for f in FILES:
        rank_filter = getFile(f)
        if bitboard & rank_filter:
            return CountPieces(getAllPawns(board) & rank_filter) == 1


def CountPieces(bitboard):
    return bin(bitboard).count("1")


def WinScore(color):
    if color == White:
        return -10 * PieceValues[King]
    if color == Black:
        return 10 * PieceValues[King]


def PseudoLegalMoves(game, color):
    for index in range(64):
        piece = game.board[index]

        if piece != Empty and piece & ColorMask == color:
            piece_pos = 0b1 << index

            for target in SingleGen(getMoves(piece_pos, game, color)):
                yield (piece_pos, target)

    if CanCastleKingSide(game, color):
        yield (getKing(game.board, color), EastOne(EastOne(getKing(game.board, color))))
    if CanCastleQueenSide(game, color):
        yield (getKing(game.board, color), WestOne(WestOne(getKing(game.board, color))))


def LegalMoves(game, color):
    for move in PseudoLegalMoves(game, color):
        if IsLegalMove(game, move):
            yield move


def IsLegalMove(game, move):
    new_game = MakeMove(game, move)
    return not is_check(new_game.board, game.to_move)


def CountLegalMoves(game, color):
    move_count = 0
    for _ in LegalMoves(game, color):
        move_count += 1
    return move_count


def IsStalemate(game):
    for _ in LegalMoves(game, game.to_move):
        return False
    return not is_check(game.board, game.to_move)


def IsCheckmate(game, color):
    for _ in LegalMoves(game, game.to_move):
        return False
    return is_check(game.board, color)


def IsSamePosition(FEN_a, FEN_b):
    FEN_a_list = FEN_a.split(' ')
    FEN_b_list = FEN_b.split(' ')
    return FEN_a_list[0] == FEN_b_list[0] and \
           FEN_a_list[1] == FEN_b_list[1] and \
           FEN_a_list[2] == FEN_b_list[2] and \
           FEN_a_list[3] == FEN_b_list[3]


def HasThreefoldRepetition(game):
    current_pos = game.position_history[-1]
    position_count = 0
    for position in game.position_history:
        if IsSamePosition(current_pos, position):
            position_count += 1
    return position_count >= 3


def Under50Move(game):
    return game.halfmove_clock >= 100


def Under75Move(game):
    return game.halfmove_clock >= 150


def HasInsufficientMaterial(game):  # TODO: other insufficient positions
    if MaterialSum(game.board, White) + MaterialSum(game.board, Black) == 2 * PieceValues[King]:
        return True
    if MaterialSum(game.board, White) == PieceValues[King]:
        if MaterialSum(game.board, Black) == PieceValues[King] + PieceValues[Knight] and \
                (getKnights(game.board, Black) != 0 or getBishops(game.board, Black) != 0):
            return True
    if MaterialSum(game.board, Black) == PieceValues[King]:
        if MaterialSum(game.board, White) == PieceValues[King] + PieceValues[Knight] and \
                (getKnights(game.board, White) != 0 or getBishops(game.board, White) != 0):
            return True
    return False


def GameEnded(game):
    return IsCheckmate(game, White) or \
           IsCheckmate(game, Black) or \
           IsStalemate(game) or \
           HasInsufficientMaterial(game) or \
           Under75Move(game)


def RandomMove(game, color):
    return choice(LegalMoves(game, color))


def EvaluatedMove(game, color):
    best_score = WinScore(color)
    best_moves = []

    for move in LegalMoves(game, color):
        evaluation = evaluate_game(MakeMove(game, move))

        if IsCheckmate(MakeMove(game, move), OpposingColor(game.to_move)):
            return [move, evaluation]

        if (color == White and evaluation > best_score) or \
                (color == Black and evaluation < best_score):
            best_score = evaluation
            best_moves = [move]
        elif evaluation == best_score:
            best_moves.append(move)

    return [choice(best_moves), best_score]


def minimax(game, color, depth=1):
    if GameEnded(game):
        return [None, evaluate_game(game)]

    [simple_move, simple_evaluation] = EvaluatedMove(game, color)

    if depth == 1 or \
            simple_evaluation == WinScore(OpposingColor(color)):
        return [simple_move, simple_evaluation]

    best_score = WinScore(color)
    best_moves = []

    for move in LegalMoves(game, color):
        his_game = MakeMove(game, move)

        if IsCheckmate(his_game, his_game.to_move):
            return [move, WinScore(his_game.to_move)]

        [_, evaluation] = minimax(his_game, OpposingColor(color), depth - 1)

        if evaluation == WinScore(OpposingColor(color)):
            return [move, evaluation]

        if (color == White and evaluation > best_score) or \
                (color == Black and evaluation < best_score):
            best_score = evaluation
            best_moves = [move]
        elif evaluation == best_score:
            best_moves.append(move)

    return [choice(best_moves), best_score]


def AlphaBeta(game, color, depth, alpha=-float('inf'), beta=float('inf')):
    if GameEnded(game):
        return [None, evaluate_game(game)]

    [simple_move, simple_evaluation] = EvaluatedMove(game, color)

    if depth == 1 or \
            simple_evaluation == WinScore(OpposingColor(color)):
        return [simple_move, simple_evaluation]

    best_moves = []

    if color == White:
        for move in LegalMoves(game, color):
            if verbose:
                print(
                    '\t' * depth + str(depth) + '. evaluating ' + PieceCodes[getPiece(game.board, move[0])] + move2str(
                        move))

            new_game = MakeMove(game, move)
            [_, score] = AlphaBeta(new_game, OpposingColor(color), depth - 1, alpha, beta)

            if verbose:
                print('\t' * depth + str(depth) + '. ' + str(score) + ' [{},{}]'.format(alpha, beta))

            if score == WinScore(OpposingColor(color)):
                return [move, score]

            if score == alpha:
                best_moves.append(move)
            if score > alpha:  # white maximizes her score
                alpha = score
                best_moves = [move]
                if alpha > beta:  # alpha-beta cutoff
                    if verbose:
                        print('\t' * depth + 'cutoff')
                    break
        if best_moves:
            return [choice(best_moves), alpha]
        else:
            return [None, alpha]

    if color == Black:
        for move in LegalMoves(game, color):
            if verbose:
                print(
                    '\t' * depth + str(depth) + '. evaluating ' + PieceCodes[getPiece(game.board, move[0])] + move2str(
                        move))

            new_game = MakeMove(game, move)
            [_, score] = AlphaBeta(new_game, OpposingColor(color), depth - 1, alpha, beta)

            if verbose:
                print('\t' * depth + str(depth) + '. ' + str(score) + ' [{},{}]'.format(alpha, beta))

            if score == WinScore(OpposingColor(color)):
                return [move, score]

            if score == beta:
                best_moves.append(move)
            if score < beta:  # black minimizes his score
                beta = score
                best_moves = [move]
                if alpha > beta:  # alpha-beta cutoff
                    if verbose:
                        print('\t' * depth + 'cutoff')
                    break
        if best_moves:
            return [choice(best_moves), beta]
        else:
            return [None, beta]


def ParseMoveCode(game, move_code):
    move_code = move_code.replace(" ", "")
    move_code = move_code.replace("x", "")

    if move_code.upper() == 'O-O' or move_code == '0-0':
        if CanCastleKingSide(game, game.to_move):
            return CastleKingSideMove(game)

    if move_code.upper() == 'O-O-O' or move_code == '0-0-0':
        if CanCastleQueenSide(game, game.to_move):
            return CastleQueenSideMove(game)

    if len(move_code) < 2 or len(move_code) > 4:
        return False

    if len(move_code) == 4:
        filter_squares = getFilter(move_code[1])
    else:
        filter_squares = AllSquares

    destination_str = move_code[-2:]
    if destination_str[0] in FILES and destination_str[1] in RANKS:
        target_square = str2bb(destination_str)
    else:
        return False

    if len(move_code) == 2:
        piece = Pawn
    else:
        piece_code = move_code[0]
        if piece_code in FILES:
            piece = Pawn
            filter_squares = getFilter(piece_code)
        elif piece_code in PieceCodes:
            piece = PieceCodes[piece_code] & PieceMask
        else:
            return False

    valid_moves = []
    for move in LegalMoves(game, game.to_move):
        if move[1] & target_square and \
                move[0] & filter_squares and \
                getPiece(game.board, move[0]) & PieceMask == piece:
            valid_moves.append(move)

    if len(valid_moves) == 1:
        return valid_moves[0]
    else:
        return False


def getPlayerMove(game):
    move = None
    while not move:
        move = ParseMoveCode(game, input())
        if not move:
            print('Invalid move!')
    return move


def getAIMove(game, depth=2):
    if verbose:
        print('Searching best move for white...' if game.to_move == White else 'Searching best move for black...')
    start_time = time()

    if FindInBook(game):
        move = getBookMove(game)
    else:
        #         move = minimax(game, game.to_move, depth)[0]
        move = AlphaBeta(game, game.to_move, depth)[0]

    end_time = time()
    if verbose:
        print(
            'Found move ' + PieceCodes[getPiece(game.board, move[0])] + ' from ' + str(bb2str(move[0])) + ' to ' + str(
                bb2str(move[1])) + ' in {:.3f} seconds'.format(end_time - start_time) + ' ({},{})'.format(
                evaluate_game(game), evaluate_game(MakeMove(game, move))))
    return move


def PrintOutcome(game):
    print(getOutcome(game))


def getOutcome(game):
    if IsStalemate(game):
        return 'Draw by stalemate'
    if IsCheckmate(game, White):
        return 'Black wins!'
    if IsCheckmate(game, Black):
        return 'White wins!'
    if HasInsufficientMaterial(game):
        return 'Draw by insufficient material!'
    if Under75Move(game):
        return 'Draw by 75-move rule!'


def PlayAsWhite(game=GamePosition()):
    print('Playing as white!')
    while True:
        PrintBoard(game.board)
        if GameEnded(game):
            break

        game = MakeMove(game, getPlayerMove(game))

        PrintBoard(game.board)
        if GameEnded(game):
            break

        game = MakeMove(game, getAIMove(game))
    PrintOutcome(game)


def PlayAsBlack(game=GamePosition()):
    print('Playing as black!')
    while True:
        PrintRotatedBoard(game.board)
        if GameEnded(game):
            break

        game = MakeMove(game, getAIMove(game))

        PrintRotatedBoard(game.board)
        if GameEnded(game):
            break

        game = MakeMove(game, getPlayerMove(game))
    PrintOutcome(game)


def WatchAIGame(game=GamePosition(), sleep_seconds=0):
    print('Watching AI-vs-AI game!')
    while True:
        PrintBoard(game.board)
        if GameEnded(game):
            break

        game = MakeMove(game, getAIMove(game))
        sleep(sleep_seconds)
    PrintOutcome(game)


def PlayAs(color):
    if color == White:
        PlayAsWhite()
    if color == Black:
        PlayAsBlack()


def PlayRandomColor():
    color = choice([White, Black])
    PlayAs(color)


def FindInBook(game):
    if game.position_history[0] != InitialFEN:
        return False

    openings = []
    book_file = open("book.txt")
    for line in book_file:
        if line.startswith(game.getMoveList()) and line.rstrip() > game.getMoveList():
            openings.append(line.rstrip())
    book_file.close()
    return openings


def getBookMove(game):
    openings = FindInBook(game)
    chosen_opening = choice(openings)
    next_moves = chosen_opening.replace(game.getMoveList(), '').lstrip()
    move_str = next_moves.split(' ')[0]
    move = [str2bb(move_str[:2]), str2bb(move_str[-2:])]
    return move


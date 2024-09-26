public class GameBoard {
    private char[][] board;
    static final int SIZE = 15;
    private static final char EMPTY = '.';

    public GameBoard() {
        board = new char[SIZE][SIZE];
        initializeBoard();
    }

    private void initializeBoard() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = EMPTY;
            }
        }
    }

    public boolean makeMove(int x, int y, char player) {
        if (isMoveLegal(x, y)) {
            board[x][y] = player;
            return true;
        }
        return false;
    }

    boolean isMoveLegal(int x, int y) {
        return x >= 0 && x < SIZE && y >= 0 && y < SIZE && board[x][y] == EMPTY;
    }

    public void printBoard() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }

    public boolean checkWin(char playerChar) {
        /***
         * Check for 5 consecutive stones in rows, columns, and both diagonals
         * */ 
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (board[i][j] == playerChar) {
                    if (checkLine(i, j, 1, 0, playerChar) || // Horizontal
                            checkLine(i, j, 0, 1, playerChar) || // Vertical
                            checkLine(i, j, 1, 1, playerChar) || // Diagonal (down-right)
                            checkLine(i, j, 1, -1, playerChar)) { // Diagonal (down-left)
                        return true;
                    }
                }
            }
        }
        return false;
    }

    private boolean checkLine(int x, int y, int dx, int dy, char playerChar) {
        int count = 0;
        for (int i = 0; i < 5; i++) {
            if (x < 0 || x >= SIZE || y < 0 || y >= SIZE || board[x][y] != playerChar) {
                return false;
            }
            x += dx;
            y += dy;
            count++;
        }
        return count == 5;
    }

    public void undoMove(int x, int y) {
        if (x >= 0 && x < SIZE && y >= 0 && y < SIZE) {
            board[x][y] = EMPTY;
        }
    }

    public char getStone(int x, int y) {
        if (x >= 0 && x < SIZE && y >= 0 && y < SIZE) {
            return board[x][y];
        }
        return '\0'; 
    }
    
    public boolean isFull() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }
}

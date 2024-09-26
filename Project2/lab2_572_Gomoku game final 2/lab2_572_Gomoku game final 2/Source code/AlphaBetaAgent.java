public class AlphaBetaAgent {

    private static final int MAX_DEPTH = 4; // adjustable depth

    public int[] decideMove(GameBoard board, char playerChar) {
        int bestVal = Integer.MIN_VALUE;
        int[] bestMove = new int[] {-1, -1};

        // Generate all possible moves
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.isMoveLegal(i, j)) {
                    // Make the move
                    board.makeMove(i, j, playerChar);

                    // Compute the value using alpha-beta pruning
                    int moveVal = minValue(board, Integer.MIN_VALUE, Integer.MAX_VALUE, 1, playerChar);

                    // Undo the move
                    board.undoMove(i, j);

                    // Update the best move
                    if (moveVal > bestVal) {
                        bestMove[0] = i;
                        bestMove[1] = j;
                        bestVal = moveVal;
                    }
                }
            }
        }
        return bestMove;
    }

    private int maxValue(GameBoard board, int alpha, int beta, int depth, char playerChar) {
        if (depth == MAX_DEPTH || board.isFull() || board.checkWin(playerChar)) {
            return evaluateBoard(board, playerChar);
        }
    
        int value = Integer.MIN_VALUE;
    
        // Generate possible moves and recursively call minValue
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.isMoveLegal(i, j)) {
                    board.makeMove(i, j, playerChar);
                    value = Math.max(value, minValue(board, alpha, beta, depth + 1, playerChar));
                    board.undoMove(i, j);
    
                    if (value >= beta) {
                        return value; // Beta cutoff
                    }
                    alpha = Math.max(alpha, value);
                }
            }
        }
        return value;
    }
    

    private int minValue(GameBoard board, int alpha, int beta, int depth, char playerChar) {
        if (depth == MAX_DEPTH || board.isFull() || board.checkWin(playerChar)) {
            return evaluateBoard(board, playerChar);
        }
    
        int value = Integer.MAX_VALUE;
    
        // Generate possible moves and recursively call maxValue
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.isMoveLegal(i, j)) {
                    board.makeMove(i, j, playerChar);
                    value = Math.min(value, maxValue(board, alpha, beta, depth + 1, playerChar));
                    board.undoMove(i, j);
    
                    if (value <= alpha) {
                        // Alpha cutoff
                        return value; 
                    }
                    beta = Math.min(beta, value);
                }
            }
        }
        return value;
    }
    
        /***
         * Board Evaluation
        *
        * Factors to consider: 
        *      > number of unbroken lines, 
        *      > potential threats.
        * Simplicity put, let's say each stone of the AI player on the board adds 1 point
        */
    private int evaluateBoard(GameBoard board, char playerChar) {
        int score = 0;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.getStone(i, j) == playerChar) {
                    score++;
                }
            }
        }
        return score;
    }
    
}

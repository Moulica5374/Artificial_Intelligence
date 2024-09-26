public class GomokuGame {

    private GameBoard board;
    private Player player1;
    private Player player2;

    public GomokuGame() {
        board = new GameBoard();
        // HumanPlayer or AIPlayer
        player1 = new HumanPlayer('X'); 
        player2 = new AIPlayer('O');
    }

    public void startGame() {
        boolean player1Turn = true;
        while (true) {
            board.printBoard();
            if (player1Turn) {
                System.out.println("Player 1's turn (X)");
                player1.makeMove(board);
            } else {
                System.out.println("Player 2's turn (O)");
                player2.makeMove(board);
            }
    
            // Check win
            if (board.checkWin(player1Turn ? 'X' : 'O')) {
                board.printBoard();
                System.out.println("Player " + (player1Turn ? "1" : "2") + " wins!");
                break;
            }
    
            // Check draw
            if (board.isFull()) {
                board.printBoard();
                System.out.println("The game is a draw!");
                break;
            }
    
            // Switch turns
            player1Turn = !player1Turn;
        }
    
        System.out.println("Game Over. Thanks for playing!");
    }
    
    public static void main(String[] args) {
        GomokuGame game = new GomokuGame();
        game.startGame();
    }
}

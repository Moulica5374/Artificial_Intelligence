public class AIPlayer extends Player {

    private AlphaBetaAgent alphaBetaAgent;

    public AIPlayer(char playerChar) {
        super(playerChar);
        this.alphaBetaAgent = new AlphaBetaAgent();
    }

    @Override
    public boolean makeMove(GameBoard board) {
        int[] move = alphaBetaAgent.decideMove(board, this.playerChar);
        return move != null && board.makeMove(move[0], move[1], this.playerChar);
    }
}

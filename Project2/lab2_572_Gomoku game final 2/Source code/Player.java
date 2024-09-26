public abstract class Player {
    protected char playerChar;

    public Player(char playerChar) {
        this.playerChar = playerChar;
    }

    abstract boolean makeMove(GameBoard board);
}

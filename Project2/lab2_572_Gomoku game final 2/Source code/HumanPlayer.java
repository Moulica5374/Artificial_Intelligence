import java.util.Scanner;

public class HumanPlayer extends Player {
    private Scanner scanner;

    public HumanPlayer(char playerChar) {
        super(playerChar);
        this.scanner = new Scanner(System.in);
    }

    @Override
    public boolean makeMove(GameBoard board) {
        int row = -1, column = -1;
        boolean validMove = false;

        while (!validMove) {
            try {
                System.out.println("Enter row number: ");
                row = Integer.parseInt(scanner.nextLine());

                System.out.println("Enter column number: ");
                column = Integer.parseInt(scanner.nextLine());

                if (row >= 0 && row < GameBoard.SIZE && column >= 0 && column < GameBoard.SIZE && board.isMoveLegal(row, column)) {
                    validMove = true;
                } else {
                    System.out.println("Invalid move. Please try again.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter valid row and column numbers.");
            }
        }

        return board.makeMove(row, column, playerChar);
    }
}

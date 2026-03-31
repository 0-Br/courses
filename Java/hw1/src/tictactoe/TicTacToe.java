package tictactoe;

public class TicTacToe
{
    int[][] board = new int[3][3];
    public TicTacToe()
    {
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++) board[i][j] = 0;
        }
    }

    private boolean check(int player)
    {
        for (int i = 0; i < 3; i++)
        {
            if ((board[i][0] == player) && (board[i][1] == player) && (board[i][2] == player)) return true;
        }
        for (int j = 0; j < 3; j++)
        {
            if ((board[0][j] == player) && (board[1][j] == player) && (board[2][j] == player)) return true;
        }
        if ((board[0][0] == player) && (board[1][1] == player) && (board[2][2] == player)) return true;
        if ((board[0][2] == player) && (board[1][1] == player) && (board[2][0] == player)) return true;
        return false;
    }

    public int place(int player, int row, int column)
    {
        if (board[row][column] != 0) return 3;
        board[row][column] = player;
        if (check(1)) return 1;
        if (check(2)) return 2;
        return 0;
    }
}
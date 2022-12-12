#include <fstream>
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

char elevation(vector<vector<char>> matrix, int i, int j) {
    if (matrix[i][j] == 'E') {
        return 'z';
    }
    if (matrix[i][j] == 'S') {
        return 'a';
    }
    return matrix[i][j];
}

class Location {
public:
    int x;
    int y;
    Location(int x, int y) {
        this->x = x;
        this->y = y;
    }
};

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("sample.txt");
    } else {
        my_file.open("input.txt");
    }

    // Read input
    if (my_file.is_open()) {
        vector<vector<char>> matrix;
        int si, sj, ei, ej = 0;

        string line;
        int r = 0;
        while (getline(my_file, line)) {
            vector<char> row;
            for (int i = 0; i < line.length(); i++) {
                char ch = line.at(i);
                row.push_back(ch);

                if (ch == 'S') {
                    si = r;
                    sj = i;
                } else if (ch == 'E') {
                    ei = r;
                    ej = i;
                }
            }
            matrix.push_back(row);
            r++;
        }
        my_file.close();

        // Start BFS to find the shortest path
        unsigned int n = matrix.size();
        unsigned int m = matrix.front().size();

        vector<vector<bool>> visited;
        vector<vector<int>> cost;
        for (int i = 0; i < n; i++) {
            visited.push_back(vector<bool>(m, false));
            cost.push_back(vector<int>(m, 0));
        }

        // Init initial state
        visited[si][sj] = true;
        queue<Location> q;
        q.push(Location(si, sj));

        int choices[][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        while (!q.empty()) {
            Location loc = q.front();
            for (auto c : choices) {
                int x = loc.x + c[0];
                int y = loc.y + c[1];
                if ((x >= 0 && x < n)
                    && (y  >= 0 && y < m)
                    && !visited[x][y]
                    && elevation(matrix, x, y) - elevation(matrix, loc.x, loc.y) <= 1) {
                    visited[x][y] = true;
                    q.push(Location(x, y));
                    cost[x][y] = cost[loc.x][loc.y] + 1;
                }
            }
            q.pop();
        }

        cout << cost[ei][ej] << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
#include <fstream>
#include <iostream>
#include <vector>
#include <tuple>

using namespace std;

bool is_invisible(vector<vector<int>> matrix, int n, int row, int col) {
    int h = matrix[row][col];
    int directions = 4;
    // up
    for (int k = row-1; k >= 0; k--) {
        if (matrix[k][col] >= h) {
            directions--;
            break;
        }
    }
    // down
    for (int k = row+1; k < n; k++) {
        if (matrix[k][col] >= h) {
            directions--;
            break;
        }
    }
    // left
    for (int k = col-1; k >= 0; k--) {
        if (matrix[row][k] >= h) {
            directions--;
            break;
        }
    }
    // right
    for (int k = col+1; k < n; k++) {
        if (matrix[row][k] >= h) {
            directions--;
            break;
        }
    }
    return directions > 0;
}

int main() {
    string line;
    ifstream myfile("input.txt");

    if (myfile.is_open()) {
        vector<vector<int>> matrix;

        while (getline(myfile, line)) {
            vector<int> v;
            for (int i = 0; i < line.length(); i++) {
                v.push_back(line.at(i) - '0');
            }
            matrix.push_back(v);
        }
        myfile.close();

        // print it
        for (auto v : matrix) {
            for (auto it : v) {
                cout << it << ' ';
            }
            cout << endl;
        }

        // processing
        int c = 0;
        int n = matrix.size();
        for (int i = n-2; i >= 1; i--) {  // row
            for (int j = n-2; j >= 1; j--) {  // column
                if (is_invisible(matrix, n, i, j)) {
                    c++;
                }
            }
        }
        cout << endl;

        c += 4*(n-1); // include edge trees
        cout << c << endl; // 1805
    } else {
        cout << "Unable to open file" << endl;
    }
}
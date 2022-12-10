#include <fstream>
#include <iostream>
#include <vector>
#include <tuple>

using namespace std;

int calculate_score(vector<vector<int>> matrix, int n, int row, int col) {
    int h = matrix[row][col];
    int score = 1;
    int val = 0;

    // up
    for (int k = row-1; k >= 0; k--) {
        if (matrix[k][col] >= h) {
            val++; // last tree it can see
            break;
        }
        val++;
    }
    score *= val;
    val = 0;

    // down
    for (int k = row+1; k < n; k++) {
        if (matrix[k][col] >= h) {
            val++;
            break;
        }
        val++;
    }
    score *= val;
    val = 0;

    // left
    for (int k = col-1; k >= 0; k--) {
        if (matrix[row][k] >= h) {
            val++;
            break;
        }
        val++;
    }
    score *= val;
    val = 0;

    // right
    for (int k = col+1; k < n; k++) {
        if (matrix[row][k] >= h) {
            val++;
            break;
        }
        val++;
    }
    score *= val;

    return score;
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
        // excluding the edge trees since scenic view is 0 due to viewing distance is 0
        int largest = -1;
        int n = matrix.size();
        for (int i = n-2; i >= 1; i--) {  // row
            for (int j = n-2; j >= 1; j--) {  // column
                int score = calculate_score(matrix, n, i, j);
                if (score > largest) {
                    largest = score;
                }
            }
        }

        cout << largest << endl; // 444528
    } else {
        cout << "Unable to open file" << endl;
    }
}
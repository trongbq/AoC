#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

vector<string> split(const string s, string delim) {
    vector<string> v;
    size_t pos = 0;
    size_t start = 0;
    while ((pos = s.find(delim, start)) != string::npos) {
        v.push_back(s.substr(start, pos - start));
        start = pos + delim.length();
    }
    v.push_back(s.substr(start));
    return v;
}

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("input_sample.txt");
    } else {
        my_file.open("input.txt");
    }

    // Read input
    if (my_file.is_open()) {
        // read input and parse coordinates
        vector<vector<string>> coords;
        string line;
        while (getline(my_file, line)) {
            coords.push_back(split(line, " -> "));
        }
        my_file.close();

        // turn coordinates into 2D array
        int lowest_point = 0; // tracking the lowest coordinate, useful to know when we reach abyss
        char map[500][600];
        for (int i = 0; i < 500; i++) {
            for (int j = 0; j < 600; j++) {
                map[i][j] = '.';
            }
        }
        for (int i = 0; i < coords.size(); i++) {
            int cx = stoi(coords[i][0].substr(0, coords[i][0].find(',')));
            int cy = stoi(coords[i][0].substr(coords[i][0].find(',')+1));
            map[cy][cx] = '#';
            if (cy > lowest_point) {
                lowest_point = cy;
            }

            for (int j = 1; j < coords[i].size(); j++) {
                int x = stoi(coords[i][j].substr(0, coords[i][j].find(',')));
                int y = stoi(coords[i][j].substr(coords[i][j].find(',')+1));

                if (cx == x) {
                    // move vertically
                    if (cy > y) { // move up
                        for (int k = cy; k >= y; k--) {
                            map[k][cx] = '#';
                        }
                    } else { // move down
                        for (int k = cy; k <= y; k++) {
                            map[k][cx] = '#';
                        }
                    }
                } else {
                    // move horizontally
                    if (cx > x) { // move left
                        for (int k = cx; k >= x; k--) {
                            map[cy][k] = '#';
                        }
                    } else { // move right
                        for (int k = cx; k <= x; k++) {
                            map[cy][k] = '#';
                        }
                    }
                }
                cx = x;
                cy = y;

                if (cy > lowest_point) {
                    lowest_point = cy;
                }
            }
        }

        // sand falling
        int c = 0;
        bool abyss = false;
        while (!abyss) {
            int sr = 0, sc = 500;

            while (true) {
                if (map[sr+1][sc] == '.') { // can move down
                    sr++;
                } else if (map[sr+1][sc-1] == '.') { // can move down-left
                    sr++;
                    sc--;
                } else if (map[sr+1][sc+1] == '.') {
                    sr++;
                    sc++;
                } else { // rest
                    map[sr][sc] = 'o';
                    c++;
                    break;
                }

                if (sr == lowest_point) {
                    abyss = true;
                    break;
                }
            }
        }

        // current map
        for (int i = 0; i < 15; i++) {
            for (int j = 485; j < 550; j++) {
                cout << map[i][j];
            }
            cout << endl;
        }

        cout << c << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
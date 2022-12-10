#include <fstream>
#include <iostream>
#include <tuple>
#include <map>
#include <vector>
#include "point.cc"

using namespace std;

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("input/sample2.txt");
    } else {
        my_file.open("input/input.txt");
    }

    if (my_file.is_open()) {
        // init the rope with 10 points
        vector<Point> rope;
        for (int i = 0; i <= 9; i++) {
            rope.push_back(Point());
        }

        // remember positions where the tail used to visit
        map<Point, bool> mem;
        mem[Point(0, 0)] = true;

        int c = 1;

        string line;
        while (getline(my_file, line)) {
            char direction = line.at(0);
            int amount = stoi(line.substr(2));

            // which direction to go?
            int x = 0;
            int y = 0;
            switch (direction) {
                case 'U':
                    y = 1;
                    break;
                case 'D':
                    y = -1;
                    break;
                case 'L':
                    x = -1;
                    break;
                case 'R':
                    x = 1;
                    break;
                default:
                    cout << "Invalid direction:" << direction << endl;
            }

            for (int step = 1; step <= amount; step++) {
                rope[0].move(1*x, 1*y);

                // moving knots and tail
                for (int i = 1; i <= 9; i++) {
                    if (!rope[i].is_touching(rope[i-1])) {
                        auto [next_x, next_y] = next_move(rope[i-1], rope[i]);
                        rope[i].move(next_x, next_y);

                        if (i == 9) {
                            // count visit position of the tail
                            Point temp(rope[i].x, rope[i].y);
                            if (mem.find(temp) == mem.end()) {
                                c++;
                                mem[temp] = true;
                            }
                        }
                    }
                }
            }
        }
        my_file.close();

        cout << "Final position of the rope:" << endl;
        for (auto k : rope) {
            cout << k;
        }
        cout << endl;

        cout << c << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
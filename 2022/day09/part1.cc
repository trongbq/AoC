#include <fstream>
#include <iostream>
#include <tuple>
#include <map>
#include "point.cc"

using namespace std;

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("input/sample1.txt");
    } else {
        my_file.open("input/input.txt");
    }

    if (my_file.is_open()) {
        Point head;
        Point tail;

        map<Point, bool> mem;
        mem[Point(0, 0)] = true;

        int c = 1;

        string line;
        while (getline(my_file, line)) {
            char direction = line.at(0);
            int amount = stoi(line.substr(2));

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

            for (int i = 1; i <= amount; i++) {
                head.move(1*x, 1*y);

                if (!tail.is_touching(head)) {
                    auto [next_x, next_y] = next_move(head, tail);
                    tail.move(next_x, next_y);

                    // count visit position
                    Point temp (tail.x, tail.y);
                    if (mem.find(temp) == mem.end()) {
                        c++;
                        mem[temp] = true;
                    }
                }
            }
        }
        my_file.close();

        cout << "Final position of head:" << head << " and tail:" << tail << endl;
        cout << c << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
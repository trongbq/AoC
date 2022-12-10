#include <fstream>
#include <iostream>
#include <math.h>

using namespace std;

int target_cycle(int cycle) {
    return 20 + 40 * ceil((cycle - 20) / 40.0);
}

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("sample.txt");
    } else {
        my_file.open("input.txt");
    }

    if (my_file.is_open()) {
        int c = 0;

        int cycles = 0;
        int current_value = 1;

        string line;
        while (getline(my_file, line)) {
            int target = target_cycle(cycles);

            if (line.rfind("noop", 0) == 0) {
                cycles++;
                if (cycles == target) {
                    c += current_value * cycles;
                }
            } else if (line.rfind("addx", 0) == 0) {
                cycles += 2;

                int val = stoi(line.substr(5));

                if (target == cycles - 1) {
                    c += current_value * (cycles-1);
                } else if (target == cycles) {
                    c += current_value * cycles;
                }

                current_value += val;
            } else {
                cout << "Unknown operation:" << line << endl;
                break;
            }
        }
        my_file.close();

        cout << c << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
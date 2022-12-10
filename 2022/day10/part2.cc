#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("sample.txt");
    } else {
        my_file.open("input.txt");
    }

    if (my_file.is_open()) {
        int current_value = 1;
        vector<int> signals;
        string line;
        while (getline(my_file, line)) {
            if (line.rfind("noop", 0) == 0) {
                signals.push_back(current_value);
            } else if (line.rfind("addx", 0) == 0) {
                signals.push_back(current_value);
                signals.push_back(current_value);

                int val = stoi(line.substr(5));
                current_value += val;
            } else {
                cout << "Unknown operation:" << line << endl;
                break;
            }
        }
        my_file.close();

        char crt[6][40] = {};
        for (int i = 0; i < 240 && i < signals.size(); i++) {
            // current position of signal and crt at certain row
            int curr_signal = signals[i];
            int curr_crt = i % 40;

            if (curr_crt == curr_signal || curr_crt == curr_signal - 1 || curr_crt == curr_signal + 1) {
                crt[i/40][curr_crt] = '#';
            } else {
                crt[i/40][curr_crt] = '.';
            }
        }

        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 40; j++) {
                cout << crt[i][j] << ' ';
            }
            cout << endl;
        }
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
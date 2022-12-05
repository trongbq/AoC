#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    string line;
    ifstream myfile("input.txt");

    int max = 0;
    int current = 0;
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            if (line.empty()) {
                if (current > max) {
                    max = current;
                }
                current = 0;
            } else {
                current += stoi(line);
            }
        }
        myfile.close();

        if (current > max) {
            max = current;
        }
        cout << max << '\n';
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

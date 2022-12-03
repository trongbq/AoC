#include <iostream>
#include <fstream>
#include <string>
#include <map>

using namespace std;

int get_priority(char c) {
    if (c >= 'a' && c <= 'z') {
        return int(c) - 'a' + 1;
    }
    return 27 + int(c) - 'A';
}

int main() {
    string line;
    ifstream myfile("input.txt");

    int total = 0;
    int count = 0;
    map<char, int> mem;

    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            count += 1;

            for (int i = 0; i < line.length(); i++) {
                char item_type = line.at(i);
                if (count == 1) {
                    if (mem.find(item_type) == mem.end()) {
                        mem[item_type] = 1;
                    }
                } else if (count == 2) {
                    if (mem.find(item_type) != mem.end()) {
                        mem[item_type] = 2;
                    }
                } else {
                    if (mem.find(item_type) != mem.end() && mem[item_type] == 2) {
                        total += get_priority(item_type);
                        break;
                    }
                }
            }

            // Reset for next group
            if (count == 3) {
                mem = {};
                count = 0;
            }
        }
        myfile.close();
       
        cout << total << '\n';
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

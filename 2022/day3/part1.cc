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
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            map<char, int> mem = {};
            int begin_second = line.length() / 2;

            for (int i = 0; i < begin_second; i++) {
                char item_type = line.at(i);
                if (mem.find(item_type) != mem.end()) {
                    mem[item_type] += 1;
                } else {
                    mem[item_type] = 1;
                }
            }

            for (int i = begin_second; i < line.length(); i++) {
                char item_type = line.at(i);
                if (mem.find(item_type) != mem.end()) {
                    total += get_priority(item_type);
                    break;
                }
            }
        }
        myfile.close();

        cout << total << '\n';
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

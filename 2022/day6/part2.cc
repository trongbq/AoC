#include <fstream>
#include <iostream>
#include <map>
#include <string>

using namespace std;

void print_map(map<char, int> mem) {
    map<char, int>::iterator it;
    cout << "> [";
    for (it = mem.begin(); it != mem.end(); it++) {
        cout << '(' << it->first << ":" << it->second << ')';
    }
    cout << ']' << endl;
}

int main() {
    string line;
    ifstream myfile("input.txt");

    if (myfile.is_open()) {
        getline(myfile, line);
        myfile.close();

        // A map contains the position of 4 recent chars so far.
        map<char, int> mem;
        for (int i = 0; i < line.length(); i++) {
            char curr = line.at(i);

            if (mem.find(curr) != mem.end()) {
                // Found duplicate char, erase from beginning to the position that latest duplicate char is found, except current one.
                int pos = mem[curr];
                for (auto it = mem.begin(); it != mem.end();) {
                    if (mem[it->first] <= pos) {
                        mem.erase(it++);
                    } else {
                        it++;
                    }
                }
            }
            mem[curr] = i;

            // Found 14 different chars - our start-of-message marker, print and exit!
            if (mem.size() == 14) {
                cout << i + 1 << endl;
                break;
            }
        }
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

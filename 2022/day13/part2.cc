#include <fstream>
#include <iostream>
#include <vector>
#include "element.h"

using namespace std;

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("sample.txt");
    } else {
        my_file.open("input.txt");
    }

    if (my_file.is_open()) {
        vector<Element> packets;
        string line;
        while (getline(my_file, line)) {
            if (line.length() == 0) {
                continue;
            }
            Element packet = Element::parse(line);
            packets.push_back(packet);
        }
        my_file.close();

        // push two dividers into the list
        Element first_div = Element::parse("[[2]]");
        Element second_div = Element::parse("[[6]]");
        packets.insert(packets.end(), {first_div, second_div});

        // sort it
        sort(packets.begin(), packets.end());

        // where are two dividers?
        int total = 1;
        for (int i = 0; i < packets.size(); i++) {
            if (packets[i] == first_div || packets[i] == second_div) {
                total *= (i+1);
            }
        }
        cout << total << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
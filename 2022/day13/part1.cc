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
        int c = 1;
        int total = 0;
        string line;
        while (getline(my_file, line)) {
            Element first = Element::parse(line);

            // read next line
            getline(my_file, line);
            Element second = Element::parse(line);

            if (first < second || first == second) {
                total += c;
            }

            // ignore empty line - a separator
            my_file.ignore(1);
            c++;
        }
        my_file.close();

        cout << total << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
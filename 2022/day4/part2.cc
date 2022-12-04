#include <iostream>
#include <fstream>
#include <string>
#include <map>

using namespace std;


int main() {
    string line;
    ifstream myfile("input.txt");

    int total = 0;
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            int comma = line.find(",");
            string first = line.substr(0, comma);
            string second = line.substr(comma+1);

            int first_dash = first.find("-");
            int first_start = stoi(first.substr(0, first_dash));
            int first_end = stoi(first.substr(first_dash+1));

            int second_dash = second.find("-");
            int second_start = stoi(second.substr(0, second_dash));
            int second_end = stoi(second.substr(second_dash + 1));

            if ((first_end >= second_start && first_end <= second_end) 
                || (second_end >= first_start && second_end <= first_end)) {
                total++;
            }
        }
        myfile.close();
       
        cout << total << '\n';
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

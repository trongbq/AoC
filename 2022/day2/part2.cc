#include <iostream>
#include <fstream>
#include <string>
#include <map>

using namespace std;

int main() {
    string line;
    ifstream myfile("input.txt");

    map<char, int> values = {
        {'A', 1}, // Rock
        {'B', 2}, // Paper
        {'C', 3}, // Scissor
    };
    map<char, int> result = {
        {'X', 0}, // lose
        {'Y', 3}, // draw
        {'Z', 6}, // win
    };
    map<char, map<char, char>> mapping = {
        {'A', {{'X', 'C'}, {'Y', 'A'}, {'Z', 'B'}}},
        {'B', {{'X', 'A'}, {'Y', 'B'}, {'Z', 'C'}}},
        {'C', {{'X', 'B'}, {'Y', 'C'}, {'Z', 'A'}}}
    };

    int score = 0;
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            char opponent_choice = line.at(0);
            char guide_want = line.at(2);

            score += values[mapping[opponent_choice][guide_want]] + result[guide_want];
        }
        myfile.close();

       
        cout << score << '\n';
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

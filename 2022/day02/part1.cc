#include <iostream>
#include <fstream>
#include <map>

using namespace std;

int main() {
    string line;
    ifstream myfile("input.txt");

    // A/X for Rock
    // B/Y for Paper
    // C/Z for Scissor
    map<char, char> winning = {
        {'A', 'Y'},
        {'B', 'Z'},
        {'C', 'X'},
    };
    map<char, char> lose = {
        {'A', 'Z'},
        {'B', 'X'},
        {'C', 'Y'},
    };
    map<char, char> draw = {
        {'A', 'X'},
        {'B', 'Y'},
        {'C', 'Z'},
    };
    map<char, int> values = {
        {'X', 1},
        {'Y', 2},
        {'Z', 3},
    };

    int score = 0;
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            char opponent_choice = line.at(0);
            char guide_choice = line.at(2);

            score += values[guide_choice];
            if (guide_choice == winning[opponent_choice]) {
                score += 6;
            } else if (guide_choice == lose[opponent_choice]) {
                // Just for demonstration and keep idea clear
                score += 0;
            } else if (guide_choice == draw[opponent_choice]) {
                score += 3;
            } else {
                cout << "INVALID" << '\n';
            }
            cout << score << '\n';
        }
        myfile.close();

       
        cout << score << '\n';
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

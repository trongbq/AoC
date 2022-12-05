#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <vector>
#include <stack>

using namespace std;

// void print_crates(stack<char> crates[4]) {
//     for (int i = 1; i < 4; i++) {
//         while (!crates[i].empty()) {
//             cout << crates[i].top();
//             crates[i].pop();
//         }
//         cout << endl;
//     }
// }

int main() {
    // Prepare data
    stack<char> crates[9];
    // crates[1] = stack<char>(deque<char>{'Z', 'N'});
    // crates[2] = stack<char>(deque<char>{'M', 'C', 'D'});
    // crates[3] = stack<char>(deque<char>{'P'});

    crates[1] = stack<char>(deque<char>{'N', 'B', 'D', 'T', 'V', 'G', 'Z', 'J'});
    crates[2] = stack<char>(deque<char>{'S', 'R', 'M', 'D', 'W', 'P', 'F'});
    crates[3] = stack<char>(deque<char>{'V', 'C', 'R', 'S', 'Z'});
    crates[4] = stack<char>(deque<char>{'R', 'T', 'J', 'Z', 'P', 'H', 'G'});
    crates[5] = stack<char>(deque<char>{'T', 'C', 'J', 'N', 'D', 'Z', 'Q', 'F'});
    crates[6] = stack<char>(deque<char>{'N', 'V', 'P', 'W', 'G', 'S', 'F', 'M'});
    crates[7] = stack<char>(deque<char>{'G', 'C', 'V', 'B', 'P', 'Q'});
    crates[8] = stack<char>(deque<char>{'Z', 'B', 'P', 'N'});
    crates[9] = stack<char>(deque<char>{'W', 'P', 'J'});

    // print_crates(crates);

    // Read steps and apply changes
    string line;
    ifstream myfile("input.txt");

    int line_count = 0;
    int start = 11;
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            line_count++;
            if (line_count < start) {
                continue;
            }

            cout << line << endl;

            smatch m;
            if (regex_search(line, m, regex("move ([0-9]+) from ([0-9]+) to ([0-9]+)"))) {
                // cout << m[0] << '=' << m[1] << ':' << m[2] << ':' << m[3] << endl;
                int amount = stoi(m[1]);
                int from  = stoi(m[2]);
                int to = stoi(m[3]);

                for (int i = 1; i <= amount; i++) {
                    if (crates[from].empty()) {
                        cout << "caught it empty" << endl;
                    }
                    crates[to].push(crates[from].top());
                    crates[from].pop();
                }
                // cout << crates[1].size() << endl;
                // cout << '>' << crates[1].top() << ':' << crates[2].top() << endl;
            } else {
                cout << "Line malformed!" << endl;
            }
        }
        cout << 'a';
        myfile.close();

        cout << "Finish!" << endl;


        for (int i = 1; i < 10; i++) {
            cout << crates[i].top();
        }
        cout << endl;
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

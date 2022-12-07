#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <stack>

using namespace std;

int main() {
    // Prepare data
    stack<char> crates[10];
    // crates[1] = stack<char>(deque<char>{'Z', 'N'});
    // crates[2] = stack<char>(deque<char>{'M', 'C', 'D'});
    // crates[3] = stack<char>(deque<char>{'P'});

    crates[1] = stack<char>(deque<char>({'N', 'B', 'D', 'T', 'V', 'G', 'Z', 'J'}));
    crates[2] = stack<char>(deque<char>{'S', 'R', 'M', 'D', 'W', 'P', 'F'});
    crates[3] = stack<char>(deque<char>{'V', 'C', 'R', 'S', 'Z'});
    crates[4] = stack<char>(deque<char>{'R', 'T', 'J', 'Z', 'P', 'H', 'G'});
    crates[5] = stack<char>(deque<char>{'T', 'C', 'J', 'N', 'D', 'Z', 'Q', 'F'});
    crates[6] = stack<char>(deque<char>{'N', 'V', 'P', 'W', 'G', 'S', 'F', 'M'});
    crates[7] = stack<char>(deque<char>{'G', 'C', 'V', 'B', 'P', 'Q'});
    crates[8] = stack<char>(deque<char>{'Z', 'B', 'P', 'N'});
    crates[9] = stack<char>(deque<char>{'W', 'P', 'J'});

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

            smatch m;
            if (regex_search(line, m, regex("move ([0-9]+) from ([0-9]+) to ([0-9]+)"))) {
                int amount = stoi(m[1]);
                int from  = stoi(m[2]);
                int to = stoi(m[3]);

                for (int i = 1; i <= amount; i++) {
                    crates[to].push(crates[from].top());
                    crates[from].pop();
                }
            } else {
                cout << "Line malformed!" << endl;
            }
        }
        myfile.close();

        // Get top of each columns
        for (int i = 1; i < 10; i++) {
            cout << crates[i].top();
        }
        cout << endl;
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

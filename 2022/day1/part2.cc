#include <iostream>
#include <fstream>
#include <string>
#include <queue>
#include <vector>

using namespace std;

int main() {
    string line;
    ifstream myfile("input.txt");

    priority_queue<int, vector<int>, greater<int>> min_q;

    int current = 0;
    if (myfile.is_open()) {
        while (getline(myfile, line)) {
            if (line.empty()) {
                // Maintain min heap size of 3.
                // If current Elf's calories greater than the top (the third Elf) then replace it,
                // else just ignore.
                cout << current << '\n';
                if (min_q.size() < 3) {
                    min_q.push(current);
                } else if (current > min_q.top()) {
                    min_q.pop();
                    min_q.push(current);
                }
                current = 0;
            } else {
                current += stoi(line);
            }
        }
        myfile.close();

        // The last Elf
        if (min_q.size() < 3) {
            min_q.push(current);
        } else if (current > min_q.top()) {
            min_q.pop();
            min_q.push(current);
        }

        // Sum of most calories in top 3 Elves
        int value = 0;
        for (;!min_q.empty(); min_q.pop()) {
            cout << min_q.top() << '\n';
            value += min_q.top();
        }
        cout << value << '\n';
    } else {
        cout << "Unable to open file" << '\n';
    }

    return 0;
}

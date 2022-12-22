#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <regex>
#include <vector>

using namespace std;

template <typename T>
string join(vector<T> const &vec) {
    if (vec.empty()) {
        return string();
    }

    return accumulate(vec.begin() + 1, vec.end(), to_string(vec[0]), [](const string &a, T b) {
        return a + ", " + to_string(b);
    });
}

int mod(int64_t a, int64_t b) {
    int r = a % b;
    return r < 0 ? r + b : r;
}

int64_t mix(vector<int64_t> numbers) {
    int n = numbers.size();
    // circle array stores index position of the original array of numbers
    vector<int> circle(n);
    iota(circle.begin(), circle.end(), 0);

    for (int i = 0; i < n; i++) {
        int64_t value = numbers[i];

        // looking for index of numbers[i] in circle array then remove it
        int from = 0;
        while (from < n) {
            if (circle[from] == i) {
                break;
            }
            from++;
        }
        circle.erase(circle.begin() + from);

        // insert it into new position
        // mod to (n-1) due to 1 removed element
        int to = mod(from + value, n - 1);
        circle.insert(circle.begin() + to, i);
    }

    // find the 0 value position
    int i0 = 0;
    while (numbers[i0] != 0) {
        i0++;
    }
    int ic0 = 0;
    while (circle[ic0] != i0) {
        ic0++;
    }

    int i1000th = circle[(ic0 + 1000) % n];
    int i2000th = circle[(ic0 + 2000) % n];
    int i3000th = circle[(ic0 + 3000) % n];
    return numbers[i1000th] + numbers[i2000th] + numbers[i3000th];
}

int64_t mix_harder(vector<int64_t> numbers) {
    int n = numbers.size();
    vector<int> circle(n);
    iota(circle.begin(), circle.end(), 0);

    int k = 0;
    while (k < 10) {
        for (int i = 0; i < n; i++) {
            int64_t value = numbers[i] * 811589153;

            // looking for index of numbers[i] in circle array then remove it
            int from = 0;
            while (from < n) {
                if (circle[from] == i) {
                    break;
                }
                from++;
            }
            circle.erase(circle.begin() + from);

            // insert it into new position
            // mod to (n-1) due to 1 removed element
            int to = mod(from + value, n - 1);
            circle.insert(circle.begin() + to, i);
        }
        k++;
    }

    int i0 = 0;
    while (numbers[i0] != 0) {
        i0++;
    }
    int ic0 = 0;
    while (circle[ic0] != i0) {
        ic0++;
    }

    int i1000th = circle[(ic0 + 1000) % n];
    int i2000th = circle[(ic0 + 2000) % n];
    int i3000th = circle[(ic0 + 3000) % n];
    return numbers[i1000th] * 811589153 + numbers[i2000th] * 811589153 + numbers[i3000th] * 811589153;
}

int main(int argc, char *argv[]) {
    ifstream my_file(argc > 1 && string(argv[1]) == "-t" ? "input_sample.txt" : "input.txt");
    if (my_file.is_open()) {
        vector<int64_t> numbers;
        string line;
        while (getline(my_file, line)) {
            numbers.emplace_back(stoi(line));
        }
        my_file.close();

        cout << "Part 1:" << mix(numbers) << endl;
        cout << "Part 2:" << mix_harder(numbers) << endl;
    } else {
        cout << "can not open file!" << endl;
    }
}

#include <fstream>
#include <iostream>
#include <unordered_map>
#include <numeric>
#include <regex>
#include <vector>

using namespace std;

const string root_mk = "root";
const string humn_mk = "humn";

struct operator_t {
    string left;
    string op;
    string right;
};

ostream& operator<<(ostream& os, const operator_t& op) {
    return os << op.left << ' ' << op.op << ' ' << op.right;
}

vector<string> split(const string s, string delim) {
    vector<string> v;
    size_t pos = 0;
    size_t start = 0;
    while ((pos = s.find(delim, start)) != string::npos) {
        v.push_back(s.substr(start, pos - start));
        start = pos + delim.length();
    }
    v.push_back(s.substr(start));
    return v;
}

long long exec(long long left, string op, long long right) {
    if (op == "+") {
        return left + right;
    } else if (op == "-") {
        return left - right;
    } else if (op == "*") {
        return left * right;
    } else if (op == "/") {
        return left / right;
    } else {
        cout << "invalid operator:" << op << endl;
        return -1;
    }
}

long long exec_reverse(long long result, string op, long long val, bool find_left) {
    if (op == "+") {
        return result - val;
    } else if (op == "-") {
        return find_left ? result + val : val - result;
    } else if (op == "*") {
        return result / val;
    } else if (op == "/") {
        return find_left ? result * val : val / result;
    } else {
        cout << "invalid operator:" << op << endl;
        return -1;
    }
}

long long calculate(unordered_map<string, long long> number_mks, unordered_map<string, operator_t> op_mks, string root) {
    while (number_mks.find(root) == number_mks.end()) {
        for (auto &[key, op] : op_mks) {
            if (number_mks.find(key) == number_mks.end()
                && number_mks.find(op.left) != number_mks.end()
                && number_mks.find(op.right) != number_mks.end()) {
                number_mks[key] = exec(number_mks[op.left], op.op, number_mks[op.right]);
            }
        }
    }
    return number_mks[root];
}

bool contains_humn_mk(unordered_map<string, operator_t> op_mks, string root) {
    if (root == humn_mk) {
        return true;
    }
    if (op_mks.find(root) == op_mks.end()) {
        return false;
    }
    operator_t op = op_mks[root];
    return contains_humn_mk(op_mks, op.left) || contains_humn_mk(op_mks, op.right);
}

long long calculate_reverse(unordered_map<string, long long> number_mks, unordered_map<string, operator_t> op_mks, string root, int64_t value) {
    if (root == humn_mk) {
        return value;
    }

    operator_t op = op_mks[root];

    // check whether left or right operand contains the humn monkey,
    // calculate value of the other operand then go to humn-contained operand
    if (contains_humn_mk(op_mks, op.left)) {
        long long rval = calculate(number_mks, op_mks, op.right);
        long long lval = exec_reverse(value, op.op, rval, true);
        return calculate_reverse(number_mks, op_mks, op.left, lval);
    }
    long long lval = calculate(number_mks, op_mks, op.left);
    long long rval = exec_reverse(value, op.op, lval, false);
    return calculate_reverse(number_mks, op_mks, op.right, rval);
}

long long find_humn_mk(unordered_map<string, long long> number_mks, unordered_map<string, operator_t> op_mks) {
    string lroot = op_mks[root_mk].left;
    string rroot = op_mks[root_mk].right;

    number_mks.erase(humn_mk);

    // get either left or right root value
    while (number_mks.find(lroot) == number_mks.end() && number_mks.find(rroot) == number_mks.end()) {
        vector<string> keys;
        for (auto &[key, _] : op_mks) {
            keys.emplace_back(key);
        }

        for (auto key : keys) {
            operator_t op = op_mks[key];
            if (number_mks.find(op.left) != number_mks.end() && number_mks.find(op.right) != number_mks.end()) {
                number_mks[key] = exec(number_mks[op.left], op.op, number_mks[op.right]);
                op_mks.erase(key);
            }
        }
    }

    if (number_mks.find(lroot) == number_mks.end()) {
        return calculate_reverse(number_mks, op_mks, lroot, number_mks[rroot]);
    }
    return calculate_reverse(number_mks, op_mks, rroot, number_mks[lroot]);
}

int main(int argc, char *argv[]) {
    ifstream my_file(argc > 1 && string(argv[1]) == "-t" ? "input_sample.txt" : "input.txt");
    if (my_file.is_open()) {
        unordered_map<string, long long> number_monkeys;
        unordered_map<string, operator_t> operator_monkeys;

        string line;
        while (getline(my_file, line)) {
            vector<string> vs = split(line, ": ");
            string right = vs[1];

            if (right.find(' ') == string::npos) {
                number_monkeys[vs[0]] = stoi(right);
            } else {
                vector<string> vr = split(right, " ");
                operator_monkeys[vs[0]] = {vr[0], vr[1], vr[2]};
            }
        }
        my_file.close();

        cout << "Part 1:" << calculate(number_monkeys, operator_monkeys, root_mk) << endl;
        cout << "Part 2:" << find_humn_mk(number_monkeys, operator_monkeys) << endl;
    } else {
        cout << "can not open file!" << endl;
    }
}

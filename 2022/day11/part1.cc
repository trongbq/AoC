#include <fstream>
#include <iostream>
#include <math.h>
#include <vector>
#include <sstream>
#include <queue>

using namespace std;

class Operation {
public:
    char op;
    int operand; // 0 means itself
    Operation(char op, int operand);
    friend ostream& operator<< (ostream& o, Operation const& p);
    int exec(int in);
};

Operation::Operation(char op, int operand) {
    this->op = op;
    this->operand = operand;
}

ostream& operator<< (ostream& o, Operation const& operation) {
    return o << "  Operation: new = old " << operation.op << ' ' << operation.operand;
}

int Operation::exec(int in) {
    int target = operand == 0 ? in : operand;

    if (op == '+') {
        return in + target;
    }
    return in * target;
}

class Monkey {
public:
    vector<int> items;
    Operation operation;
    int test_condition;
    int true_target;
    int false_target;
    int inspection_count;

    Monkey(vector<int> items, Operation op, int test, int true_target, int false_target);
    friend ostream& operator<< (ostream& o, Monkey const& p);
    int test(int lvl);
};

Monkey::Monkey(vector<int> items, Operation op, int test, int true_target, int false_target) : operation(op.op, op.operand) {
    this->items = items;
    this->test_condition = test;
    this->true_target = true_target;
    this->false_target = false_target;
    this->inspection_count = 0;
}

ostream& operator<< (ostream& o, Monkey const& m) {
    string s;
    for (auto it: m.items) {
        s += ", " + to_string(it);
    }
    if (s.size() > 2) {
        s = s.substr(2); // remove comma and space in the beginning
    }
    return o << "  Starting items: " << s << endl
             << m.operation << endl
             << "  Test: divisible by " << m.test_condition << endl
             << "    If true: throw to monkey " << m.true_target << endl
             << "    If false: throw to monkey " << m.false_target;
}

int Monkey::test(int lvl) {
    this->inspection_count++;
    return lvl % test_condition == 0 ? true_target : false_target;
}

const string WHITESPACE = " \n\r\t\f\v";

string ltrim(const std::string &s)
{
    size_t start = s.find_first_not_of(WHITESPACE);
    return (start == std::string::npos) ? "" : s.substr(start);
}

string rtrim(const std::string &s)
{
    size_t end = s.find_last_not_of(WHITESPACE);
    return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

string trim(const std::string &s) {
    return rtrim(ltrim(s));
}

vector<int> parse_items(string s) {
    vector<int> items;
    stringstream ss(s);
    string str;
    while (getline(ss, str, ',')) {
        items.push_back(stoi(trim(str)));
    }
    return items;
}

int main (int argc, char *argv[]) {
    ifstream my_file;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("sample.txt");
    } else {
        my_file.open("input.txt");
    }

    // Read input and start simple parsing
    if (my_file.is_open()) {
        vector<Monkey> monkeys;

        string line;
        while (getline(my_file, line)) {
            // read items
            getline(my_file, line);
            string item_str = line.substr(string("  Starting items: ").size());
            vector<int> items = parse_items(item_str);

            // get operation
            getline(my_file, line);
            string op_str = line.substr(string("  Operation: new = old ").size());
            char op = op_str.at(0);
            string operand_str = op_str.substr(2);
            int operand = 0;
            if (operand_str != "old") {
                operand = stoi(operand_str);
            }
            Operation operation (op, operand);

            // get test condition
            getline(my_file, line);
            int test_condition = stoi(line.substr(string("  Test: divisible by ").size()));

            // get test true target
            getline(my_file, line);
            int true_target = stoi(line.substr(string("    If true: throw to monkey ").size()));

            // get test false target
            getline(my_file, line);
            int false_target = stoi(line.substr(string("    If false: throw to monkey ").size()));

            Monkey monkey (items, operation, test_condition, true_target, false_target);
            monkeys.push_back(monkey);

            // Skip empty line for next parsing
            getline(my_file, line);
        }
        my_file.close();

        // Display debug parsing
        for (int i = 0; i < monkeys.size(); i++) {
            cout << "Monkey " << i << endl;
            cout << monkeys[i] << endl << endl;
        }

        // Start 20 rounds
        for (int r = 1; r <= 20; r++) {
            for (int i = 0; i < monkeys.size(); i++) {
                int size = monkeys[i].items.size();
                for (auto item : monkeys[i].items) {
                    int worry_level = round(monkeys[i].operation.exec(item) / 3);
                    int next_monkey = monkeys[i].test(worry_level);
                    monkeys[next_monkey].items.push_back(worry_level);
                }
                monkeys[i].items.erase(monkeys[i].items.begin(), monkeys[i].items.begin() + size);
            }
        }

        // Result
        priority_queue<int, vector<int>, greater<int>> min_q;
        for (auto m : monkeys) {
            if (min_q.size() < 2) {
                min_q.push(m.inspection_count);
            } else if (m.inspection_count > min_q.top()){
                min_q.pop();
                min_q.push(m.inspection_count);
            }
        }
        int monkey_business = 1;
        cout << min_q.top() << endl;
        monkey_business *= min_q.top();
        min_q.pop();
        cout << min_q.top() << endl;
        monkey_business *= min_q.top();

        cout << monkey_business << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
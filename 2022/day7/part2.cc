#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

class Node {
public:
    string name;
    int size;
    Node *parent;
    vector<Node> children;
    bool is_dir;

    Node(string name, bool dir);

    Node(string name, int size, bool dir);

    void add_child(Node child);
};

Node::Node(string n, bool dir) {
    name = n;
    size = -1;
    is_dir = dir;
    parent = nullptr;
}

Node::Node(string n, int s, bool dir) {
    name = n;
    size = s;
    is_dir = dir;
    parent = nullptr;
}

void Node::add_child(Node child) {
    child.parent = this;
    children.push_back(child);
}

void print_content(Node *node, int gap) {
    gap += 2;
    if (!node->is_dir) {
        cout << string(gap, ' ') << " - " << node->size << ' ' << node->name << endl;
    } else {
        cout << string(gap, ' ') << " - " << node->name << "(" << node->size << ")" << endl;
        for (int i = 0; i < node->children.size(); i++) {
            print_content(&node->children[i], gap);
        }
    }
}

int fill_node_size(Node *node) {
    if (!node->is_dir || node->size != -1) {
        return node->size;
    }

    int s = 0;
    for (int i = 0; i < node->children.size(); i++) {
        s += fill_node_size(&node->children[i]);
    }
    node->size = s;

    return s;
}


Node* find_dir(Node *node, Node *smallest, int target) {
    if (!node->is_dir) {
        return smallest;
    }

    for (int i = 0; i < node->children.size(); i++) {
        if (node->children[i].is_dir) {
            if (node->children[i].size >= target) {
                if (node->children[i].size < smallest->size) {
                    smallest = &node->children[i];
                }

                // go deeper
                Node *temp = find_dir(&node->children[i], smallest, target);
                if (temp->size < smallest->size) {
                    smallest = temp;
                }
            }
        }
    }
    return smallest;
}

int main() {
    string line;
    ifstream myfile("input.txt");

    if (myfile.is_open()) {
        Node root("/", true);
        Node *current = 0;

        while (getline(myfile, line)) {
            if (line.rfind('$', 0) == 0) {
                // command
                string cmd = line.substr(2);
                if (cmd.rfind("cd", 0) == 0) {
                    string arg = cmd.substr(3);
                    if (arg == "/") {
                        current = &root;
                    } else if (arg == "..") {
                        current = current->parent;
                    } else {
                        // find the directory in the current directory to go into
                        bool found = false;
                        for (int i = 0; i < current->children.size(); i++) {
                            if (current->children[i].name == arg) {
                                current = &current->children[i];
                                found = true;
                                break;
                            }
                        }

                        if (!found) {
                            cout << "Can not find the target directory:" << cmd << endl;
                            return 1;
                        }
                    }
                } else if (cmd.rfind("ls", 0) == 0) {
                    // Read the next lines for result, stop when encounter a command
                    string result_line;
                    streampos prev_pos = myfile.tellg();
                    while (getline(myfile, result_line)) {
                        if (result_line.rfind('$') != 0) {
                            if (result_line.rfind("dir", 0) == 0) {
                                // a directory
                                string name = result_line.substr(result_line.find(" ") + 1);
                                current->add_child(Node(name, true));
                            } else {
                                // a file
                                int pos = result_line.find(" ");
                                string name = result_line.substr(pos + 1);
                                int size = stoi(result_line.substr(0, pos));
                                current->add_child(Node(name, size, false));
                            }
                        } else {
                            myfile.seekg(prev_pos);
                            break;
                        }

                        prev_pos = myfile.tellg();
                    }

                } else {
                    cout << "Unknown command:" << cmd << endl;
                }
            } else {
                cout << "Unexpected line:" << line << endl;
            }
        }

        fill_node_size(&root);

        cout << "$ tree ." << endl;
        print_content(&root, 0);

        int target = 30000000 - (70000000 - root.size);
        Node *smallest = find_dir(&root, &root, target);
        cout << "Found:" << smallest->size << endl;
    } else {
        cout << "Unable to open file" << endl;
    }
}
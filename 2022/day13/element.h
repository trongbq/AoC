#include <iostream>
#include <vector>

using namespace std;

enum ElementType {INT, LIST, EMPTY};

class Element {
public:
    int value;
    vector<Element> values;
    ElementType type;
    Element();
    Element(int val);
    Element(vector<Element> vs);
    static Element parse(string line);
    static tuple<Element, int> parse_content(string line, int start);
    friend ostream& operator<< (ostream& o, Element const& e);
    friend bool operator< (const Element& e1, const Element& e2);
    friend bool operator== (const Element& e1, const Element& e2);
    static bool less_than_list(const Element& e1, const Element& e2);
    static bool equal_list(const Element& e1, const Element& e2);
};

Element::Element() {
    this->type = EMPTY;
}

Element::Element(int val) {
    this->value = val;
    this->type = INT;
}

Element::Element(vector<Element> vs) {
    this->values = vs;
    this->type = LIST;
}

tuple<Element, int> Element::parse_content(string line, int start) {
    int i = line.at(start) == ',' ? start+1 : start;

    char ch = line.at(i);
    if (ch == '[') {
        // peek at next char
        if (line.at(i+1) == ']') {
            return {{}, i+2};
        }

        vector<Element> v;
        do {
            i++;
            auto [elem, next] = parse_content(line, i);
            v.push_back(elem);
            i = next;
        } while (i < line.length() && line.at(i) != ']');
        return {v, i+1};
    } else if (ch == ']') {
        return {{}, i+1};
    } else {
        string num;
        while (isdigit(line.at(i))) {
            num.push_back(line.at(i));
            i++;
        }
        return {{stoi(num)}, i};
    }
}

Element Element::parse(string line) {
    auto [elem, idx] = Element::parse_content(line, 0);
    return elem;
}

ostream& operator<< (ostream& o, Element const& e) {
    if (e.type == INT) {
        o << e.value;
    } else if (e.type == LIST) {
        o << '[';
        for (int i = 0; i < e.values.size(); i++) {
            o << e.values[i];
            if (i != e.values.size()-1) {
                o << ',';
            }
        }
        o << ']';
    } else {
        o << "[]";
    }
    return o;
}

bool Element::less_than_list(const Element &e1, const Element &e2) {
    int i = 0;
    while (i < e1.values.size() && i < e2.values.size()) {
        if (e1.values[i] == e2.values[i]) {
            i++;
            continue;
        }
        return e1.values[i] < e2.values[i];
    }
    return e1.values.size() < e2.values.size();
}

bool operator< (const Element& e1, const Element& e2) {
    if (e1.type == INT && e2.type == INT) {
        return e1.value < e2.value;
    }
    if (e1.type == INT && e2.type == LIST) {
        return Element::less_than_list(Element(vector<Element>({e1})), e2);
    }
    if (e1.type == INT && e2.type == EMPTY) {
        return false;
    }

    if (e1.type == LIST && e2.type == INT) {
        return Element::less_than_list(e1, Element(vector<Element>({e2})));
    }
    if (e1.type == LIST && e2.type == LIST) {
        return Element::less_than_list(e1, e2);
    }
    if (e1.type == LIST && e2.type == EMPTY) {
        return false;
    }

    if (e1.type == EMPTY && e2.type == INT) {
        return true;
    }
    if (e1.type == EMPTY && e2.type == EMPTY) {
        return true;
    }
    if (e1.type == EMPTY && e2.type == LIST) {
        return true;
    }

    return false;
}

bool Element::equal_list(const Element &e1, const Element &e2) {
    int i = 0;
    while (i < e1.values.size() && i < e2.values.size()) {
        if (!(e1.values[i] == e2.values[i])) {
            return false;
        }
        i++;
    }
    return e1.values.size() == e2.values.size();
}

bool operator== (const Element& e1, const Element& e2) {
    if (e1.type == INT && e2.type == INT) {
        return e1.value == e2.value;
    }
    if (e1.type == INT && e2.type == LIST) {
        return Element::equal_list(Element(vector<Element>({e1})), e2);
    }
    if (e1.type == INT && e2.type == EMPTY) {
        return false;
    }

    if (e1.type == LIST && e2.type == INT) {
        return Element::equal_list(e1, Element(vector<Element>({e2})));
    }
    if (e1.type == LIST && e2.type == LIST) {
        return Element::equal_list(e1, e2);
    }
    if (e1.type == LIST && e2.type == EMPTY) {
        return false;
    }

    if (e1.type == EMPTY && e2.type == INT) {
        return false;
    }
    if (e1.type == EMPTY && e2.type == EMPTY) {
        return true;
    }
    if (e1.type == EMPTY && e2.type == LIST) {
        return false;
    }

    return false;
}
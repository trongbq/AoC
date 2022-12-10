#include "point.h"

using namespace std;

Point::Point() {
    x = 0;
    y = 0;
}

Point::Point(int xx, int yy) {
    x = xx;
    y = yy;
}

ostream& operator<< (ostream& o, Point const& p) {
    return o << '(' << p.x << ',' << p.y << ')';
}

bool Point::operator<(const Point &p) const {
    if (x == p.x) {
        return y < p.y;
    }
    return x < p.x;
}

void Point::move(int xx, int yy) {
    x += xx;
    y += yy;
}

bool Point::is_touching(Point p) {
    int gap = max(abs(x - p.x), abs(y - p.y)); // Chebyshev distance
    return gap <= 1;
}

tuple<int, int> next_move(Point head, Point tail) {
    // random moves to find the touching point
    tuple<int, int> diagonal_choices[] = {
            {-1, -1},
            {-1, 1},
            {1, -1},
            {1, 1},
    };
    tuple<int, int> adj_choices[] = {
            {-1, 0},
            {1, 0},
            {0, -1},
            {0, 1}
    };

    tuple<int, int> *choices = (head.x != tail.x && head.y != tail.y) ? diagonal_choices : adj_choices;

    for (int i = 0; i < 4; i++) {
        Point temp (tail.x, tail.y);
        tuple<int, int> *p = choices + i;

        temp.move(get<0>(*p), get<1>(*p));
        if (temp.is_touching(head)) {
            return *p;
        }
    }

    return {999999, 999999};
}
#include <iostream>

using namespace std;

class Point {
public:
    int x;
    int y;
    Point();
    Point(int xx, int yy);
    void move(int xx, int yy);
    bool is_touching(Point p);
    friend ostream& operator<< (ostream& o, Point const& p);
    bool operator <(const Point& p) const;
};
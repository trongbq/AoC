#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <regex>

using namespace std;

class Point2D {
public:
    int x;
    int y;
    Point2D() {
        this->x = 0;
        this->y = 0;
    }
    Point2D(int x, int y) {
        this->x = x;
        this->y = y;
    }
    friend bool operator< (const Point2D &p1, const Point2D &p2) {
        if (p1.x == p2.x) {
            return p1.y < p2.y;
        }
        return p1.x < p2.x;
    }
    int distance(const Point2D& c) {
        return abs(this->x - c.x) + abs(this->y - c.y);
    }
};

class Pair {
public:
    Point2D sensor;
    Point2D beacon;
    Pair(Point2D s, Point2D b) {
        this->sensor = s;
        this->beacon = b;
    }
};

int main (int argc, char *argv[]) {
    ifstream my_file;
    int y = 0;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("input_sample.txt");
        y = 10;
    } else {
        my_file.open("input.txt");
        y = 2000000;
    }

    if (my_file.is_open()) {
        // reading data
        vector<Pair> data;

        string rx = R"(Sensor at x=([\-0-9]+), y=([\-0-9]+): closest beacon is at x=([\-0-9]+), y=([\-0-9]+))";
        string line;
        while (getline(my_file, line)) {
            smatch m;
            if (regex_search(line, m, regex(rx))) {
                Point2D sensor = Point2D(stoi(m[1]), stoi(m[2]));
                Point2D beacon = Point2D(stoi(m[3]), stoi(m[4]));
                data.push_back(Pair(sensor, beacon));
            } else {
                cout << "Can not parse line:" << line << endl;
            }
        }
        my_file.close();

//        for (auto p : data) {
//            cout << p.sensor.x << ":" << p.sensor.y << ":" << p.beacon.x << ":" << p.beacon.y << endl;
//        }

        // start doing some real work
        map<int, bool> imp; // store list of coordinates that are impossible to have beacon there
        for (int i = 0; i < data.size(); i++) {
            Point2D sensor = data[i].sensor;
            Point2D beacon = data[i].beacon;

            // project sensor location to the line y
            Point2D sensor_proj = Point2D(sensor.x, y);

            int sb_dist = sensor.distance(beacon);
            int sp_dist = sensor.distance(sensor_proj);
            int remain = sb_dist - sp_dist;
            if (remain >= 0) {
                // toward two sides (go left and right) from the projection point x
                for (int x = sensor_proj.x - remain; x <= sensor_proj.x + remain; x++) {
                    imp[x] = true;
                }
            }
        }

        // remove points where beacons found on the line
        for (int i = 0; i < data.size(); i++) {
            if (data[i].beacon.y == y && imp.find(data[i].beacon.x) != imp.end()) {
                imp.erase(data[i].beacon.x);
            }
        }
        cout << imp.size() << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
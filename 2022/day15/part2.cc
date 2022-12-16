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
    int distance(const Point2D& c) const {
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

class Segment {
public:
    int from;
    int to;
    Segment(int f, int t) {
        this->from = f < 0 ? 0 : f;
        this->to = t;
    }
    bool operator< (const Segment &s) const {
        if (this->from == s.from) {
            return this->to < s.to;
        }
        return this->from < s.from;
    }
};

int main (int argc, char *argv[]) {
    ifstream my_file;
    int64_t max_y;
    if (argc > 1 && string(argv[1]) == "-d") {
        my_file.open("input_sample.txt");
        max_y = 20;
    } else {
        my_file.open("input.txt");
        max_y = 4000000;
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

        // start doing some real work
        for (int y = 0; y <= max_y; y++) {
            // segment list contains all segment of where beacons can not be in this line y
            vector<Segment> segments;
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
                    segments.push_back(Segment(sensor_proj.x - remain, sensor_proj.x + remain));
                }
            }

            sort(segments.begin(), segments.end());

            // Check all segments to see if any point x that those segments do not cover
            // -> that the point x we're looking for.
            int curr = 0;
            for (int i = 1; i < segments.size(); i++) {
                if (segments[i].from - segments[curr].to > 1) {
                    cout << "FOUND:" << y << ":" << segments[i-1].to << "-" << segments[i].from << endl;
                    cout << "x=" << segments[i].from - 1 << ", y=" << y << endl;

                    // avoid overflow
                    unsigned long freq = (segments[i].from - 1);
                    freq = freq * 4000000 + y;
                    cout << freq << endl;
                    return 0;
                }
                if (segments[curr].to < segments[i].to) {
                    curr = i;
                }
            }
        }
        cout << "XX" << endl;
    } else {
        cout << "Unable to open file" << endl;
    }

    return 0;
}
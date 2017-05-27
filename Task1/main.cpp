//
// Created by mopkobka on 20.05.17.
//

#include <iostream>
#include <cstring>
#include <opencv2/opencv.hpp>
#include <cmath>
#include "Clustering.h"

using cv::imread;
using cv::imwrite;
using cv::Mat;
using cv::Vec3f;
using cv::Vec3b;
using std::abs;
using std::cos;
using std::cout;
using std::endl;
using std::pair;
using std::pow;
using std::sin;
using std::strcmp;
using std::string;
using std::sqrt;
using std::tan;
typedef pair<int, int> coordinate;

class State {
public:
    bool reduce;
    bool rotate;
    bool segment;
    string im_path;
    State(): reduce(false), rotate(false), segment(false), im_path("") {}
};

State parse_args(int num, char **args) {
    State state;
    for (int i = 1; i < num; i++) {
        if (strcmp(args[i], "--reduce") == 0)
            state.reduce = true;
        else if (strcmp(args[i], "--rotate") == 0)
            state.rotate = true;
        else if (strcmp(args[i], "--segment") == 0)
            state.segment = true;
        else if (strcmp(args[i], "--help") == 0){
            cout << "task1 IMAGE [--reduce] [--rotate] [--segment] [--help]" << endl;
            cout << "IMAGE:     " << "Path to image" << endl;
            cout << "--reduce:  " << "Reduce the image sqrt(2) times" << endl;
            cout << "--rotate:  " << "Rotate the image 28 degrees" << endl;
            cout << "--segment: " << "Segment the image" << endl;
            cout << "--help:    " << "Show this message" << endl;
            exit(0);
        }
        else state.im_path = args[i];
    }
    if (state.im_path == "") {
        cout << "No input image" << endl;
        cout << "Type --help to see help info" << endl;
        exit(-1);
    }
    return state;
}

// Bicubic interpolation, edges type: mirror
Vec3b bicubic(Mat &image, int x, int y){
    Vec3b pixel(0, 0, 0);
    // Close pixels, radius=1
    int *x_close = new int[2] {abs(x - 1), (x < image.rows - 1) ? x + 1 : image.rows - 2},
        *y_close = new int[2] {abs(y - 1), (y < image.cols - 1) ? y + 1 : image.cols - 2};
    // Far pixels, radius=3
    int *x_far = new int[2] {abs(x - 3), (x < image.rows - 3) ? x + 3 : 2 * image.rows - x - 5},
        *y_far = new int[2] {abs(y - 3), (y < image.cols - 3) ? y + 3 : 2 * image.cols - y - 5};
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            pixel += image.at<Vec3b>(x_close[i], y_close[j]) / 6 +
                     image.at<Vec3b>(x_close[i], y_far[j]) / 48 +
                     image.at<Vec3b>(x_far[i], y_close[j]) / 48 +
                     image.at<Vec3b>(x_far[i], y_far[j]) / 48;
    return pixel;
}

// Reduce image sqrt(2) times using bicubic interpolation
Mat reduce_image(Mat &image) {
    Mat reduced(image.rows / sqrt(2), image.cols / sqrt(2), image.type());

    #pragma omp parallel for
    for (int i = 0; i < reduced.rows; i++)
        for (int j = 0; j < reduced.cols; j++) {
            int x = i * sqrt(2), y = j * sqrt(2);
            reduced.at<Vec3b>(i, j) = image.at<Vec3b>(x, y) / 2 + bicubic(image, x, y) / 2;
        }
    return reduced;
}

// Rotate image 28 degrees, with black borders
Mat rotate_image(Mat &image) {
    int h = image.rows, w = image.cols;
    double a = 28. * 3.1418 / 180.;
    double cos_a = cos(a), sin_a = sin(a);  // For better performance
    double x_off = -w * sin_a * cos_a, y_off = w * pow(sin_a, 2.);  // For better performance
    Mat rotated(h * cos(a) + w * sin(a), w * cos(a) + h * sin(a), image.type());

    #pragma omp parallel for
    for (int i = 0; i < rotated.rows; i++)
        for (int j = 0; j < rotated.cols; j++) {
            double x = i * cos_a + j * sin_a + x_off;
            double y = j * cos_a - i * sin_a + y_off;
            if (not (x < 0 || x > image.rows - 1 || y < 0 || y > image.cols - 1))
                rotated.at<Vec3b>(i, j) = image.at<Vec3b>(x, y);
        }
    return rotated;
}

// Segment image for N clusters
Mat segment_image(Mat &image, int n_clusters=2) {
    Clustering C(image);
    C.Segment(n_clusters);
    Mat segmented(image.rows, image.cols, image.type());

    #pragma omp parallel for
    for (int i = 0; i < segmented.rows; i++)
        for (int j = 0; j < segmented.cols; j++) {
            int color = C.segmented->at<int>(i, j) * 255. / (n_clusters - 1);
            segmented.at<Vec3b>(i, j) = Vec3b(color, color, color);
        }
    return segmented;
}

int main(int argc, char** argv) {
    State state = parse_args(argc, argv);
    Mat image = imread(state.im_path, CV_LOAD_IMAGE_COLOR);
    if (state.reduce) {
        cout << "Start reduce" << endl;
        imwrite("reduced.jpg", reduce_image(image));
        cout << "Reduce done, saved to `reduced.jpg`" << endl;
    }
    if (state.rotate) {
        cout << "Start rotate" << endl;
        imwrite("rotated.jpg", rotate_image(image));
        cout << "Rotate done, saved to `rotated.jpg`" << endl;
    }
    if (state.segment) {
        cout << "Start segment" << endl;
        imwrite("segmented.jpg", segment_image(image));
        cout << "Segment done, saved to `segmented.jpg`" << endl;
    }
    return 0;
}

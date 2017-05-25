//
// Created by mopkobka on 25.05.17.
//

#include <iostream>
#include <opencv2/opencv.hpp>
#include <random>
#include <vector>

using cv::Mat;
using cv::Vec3b;
using std::pow;
using std::rand;
using std::srand;
using std::sqrt;
using std::vector;

double VecDistance(Vec3b a, Vec3b b) {
    return sqrt(pow(double(a[0]) - b[0], 2)
                + pow(double(a[1]) - b[1], 2)
                + pow(double(a[2]) - b[2], 2));
}

class Cluster {
public:
    vector<Vec3b> pixels;
    Vec3b center, prev_center;

    Cluster() {};
    Cluster(Vec3b pix) : center(pix), prev_center(pix) {}

    void AddPoint(Vec3b pix) {
        pixels.push_back(pix);
    }

    double Dist(Vec3b point) {
        return VecDistance(point, prev_center);
    }

    double UpdateCenter() {
        double p1 = 0, p2 = 0, p3 = 0; // Many pixels -> very large sum
        for (Vec3b pix: pixels) {
            p1 += pix[0];
            p2 += pix[1];
            p3 += pix[2];
        }
        center = Vec3b(p1 / pixels.size(), p2 / pixels.size(), p3 / pixels.size());
        double d = VecDistance(center, prev_center);
        prev_center = Vec3b(center);
        pixels.clear();
        return d;
    }

};

class Clustering {
public:
    Mat *segmented, *image;

    Clustering(Mat &image) : image(&image) {
        this->segmented = new Mat(image.rows, image.cols, CV_16UC2);
    }

    Mat* Segment(int n_clusters = 2) {
        srand(time(NULL));
        Cluster *clusters = new Cluster[n_clusters];
        for (int i = 0; i < n_clusters; i++)
            clusters[i] = Cluster(Vec3b(rand() % 255, rand() % 255, rand() % 255));
        float center_offset;
        int step = 0;

        do {
            for (int x = 0; x < image->rows; x++)
                for (int y = 0; y < image->cols; y++) {
                    Vec3b pix = image->at<Vec3b>(x, y);
                    double min_dist = clusters[0].Dist(pix);
                    int cluster_num = 0;
                    for (int c = 1; c < n_clusters; c++) {
                        double dist = clusters[c].Dist(pix);
                        if (dist < min_dist) {
                            min_dist = dist;
                            cluster_num = c;
                        }
                    }
                    clusters[cluster_num].AddPoint(pix);
                    segmented->at<int>(x, y) = cluster_num;
                }

            center_offset = 0;
            for (int i = 0; i < n_clusters; i++)
                center_offset += clusters[i].UpdateCenter();
        } while (center_offset > n_clusters || step++ > 20);

        return segmented;
    }
};
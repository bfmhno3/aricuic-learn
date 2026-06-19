#include <opencv2/opencv.hpp>
#include <iostream>
#include <iomanip>

/**
 * @brief 将输入图像转换为 im2col 矩阵
 * @param input 输入图像
 * @param kh 卷积核高度
 * @param kw 卷积核宽度
 * @param output 输出矩阵（CV_64F），尺寸为 (channels * kh * kw) x (h_out * w_out)，
                 其中 h_out = input.rows - kh + 1, w_out = input.cols - kw + 1
 */
void im2col(const cv::Mat& input, int kh, int kw, cv::Mat& output) {
    int h_out = input.rows - kh + 1; // 卷积后输出的高度（假设 stride=1, padding=0）
    int w_out = input.cols - kw + 1; // 卷积后输出的宽度
    int channels = input.channels(); // 输入图像的通道数

    // 计算转换后矩阵的行数和列数
    int rows = channels * kh * kw; // 每一列代表一个感受野，其元素数量 = 通道数 * 核高 * 核宽
    int cols = h_out * w_out; // 总共能滑动出多少个感受野 = 输出特征图的总像素数
    output.create(rows, cols, CV_64F); // 创建双精度浮点型输出矩阵

    for (int h = 0; h < h_out; h++) { 
        for (int w = 0; w < w_out; w++) {
            // col_idx 代表第几个滑动窗口
            int col_idx = h * w_out + w;

            for (int i = 0; i < kh; i++) {
                for (int j = 0; j < kw; j++) {
                    // row_idx 代表窗口内部像素展平后的索引位置
                    int row_idx = i * kw + j;

                    // 将原图中 (h+i, w+j) 位置的像素复制到新矩阵对应的行列
                    output.at<double>(row_idx, col_idx) =
                        input.at<double>(h + i, w + j);
                }
            }
        }
    }
}

int main() {
    cv::Mat input = (cv::Mat_<double>(4, 4) <<
        1,  2,  3,  4,
        5,  6,  7,  8,
        9, 10, 11, 12,
       13, 14, 15, 16);

    int kh = 3, kw = 3;

    std::cout << "Input matrix (4x4):\n";
    for (int i = 0; i < input.rows; i++) {
        for (int j = 0; j < input.cols; j++) {
            std::cout << std::setw(4) << input.at<double>(i, j);
        }
        std::cout << "\n";
    }

    cv::Mat col_matrix;
    im2col(input, kh, kw, col_matrix);

    std::cout << "\nim2col output (" << col_matrix.rows << "x" << col_matrix.cols << "):\n";
    std::cout << "Each column = one 3x3 receptive field flattened\n\n";

    for (int i = 0; i < col_matrix.rows; i++) {
        for (int j = 0; j < col_matrix.cols; j++) {
            std::cout << std::setw(4) << col_matrix.at<double>(i, j);
        }
        std::cout << "\n";
    }

    std::cout << "\nData duplication analysis:\n";
    std::cout << "Input elements: " << input.rows * input.cols << "\n";
    std::cout << "Column matrix elements: " << col_matrix.rows * col_matrix.cols << "\n";
    std::cout << "Duplication factor: " << (double)(col_matrix.rows * col_matrix.cols) / (input.rows * input.cols) << "\n";
    std::cout << "Expected (Kh*Kw): " << kh * kw << "\n";

    std::cout << "\nExample: element 6 appears in these positions:\n";
    for (int i = 0; i < col_matrix.rows; i++) {
        for (int j = 0; j < col_matrix.cols; j++) {
            if (col_matrix.at<double>(i, j) == 6) {
                std::cout << "  col_matrix[" << i << "][" << j << "]\n";
            }
        }
    }

    return 0;
}

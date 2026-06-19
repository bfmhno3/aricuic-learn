#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>
#include <filesystem>

namespace fs = std::filesystem;

/**
 * @brief 滑动窗口卷积实现
 * @param input 输入图像（单通道灰度图，CV_64F）
 * @param kernel 卷积核（CV_64F）
 * @param output 输出图像（CV_64F）
 * @note 严格来说这是互相关 Cross-Correlation，因为没有翻转卷积核，
         但在深度学习中通常也称为卷积 Convolution
 */
void conv2d_manual(const cv::Mat& input, const cv::Mat& kernel, cv::Mat& output) {
    int kh = kernel.rows; // 卷积核高度
    int kw = kernel.cols; // 卷积核宽度

    // 计算输出矩阵的尺寸（Valid 模式：不进行任何图像边缘填充）
    int h_out = input.rows - kh + 1;
    int w_out = input.cols - kw + 1;

    // 创建输出矩阵，数据类型为双精度浮点型（CV_64F）并清零
    output.create(h_out, w_out, CV_64F);
    output.setTo(0);

    for (int h = 0; h < h_out; h++) { // 遍历输出图像的行
        for (int w = 0; w < w_out; w++) { // 遍历输出图像的列
            double sum = 0;
            for (int i = 0; i < kh; i++) { // 遍历卷积核的行
                for (int j = 0; j < kw; j++) { // 遍历卷积核的列
                    sum += kernel.at<double>(i, j) * input.at<double>(h + i, w + j);
                }
            }
            output.at<double>(h, w) = sum; // 将结果存入对应的位置
        }
    }
}

int main() {
    // 通过 __FILE__ 获取源文件所在目录，拼接图片绝对路径
    fs::path src_dir = fs::path(__FILE__).parent_path();
    fs::path img_path = src_dir / "test_image.png";

    // 读取为单通道灰度图
    cv::Mat img = cv::imread(img_path.string(), cv::IMREAD_GRAYSCALE);
    // 检查图片是否加载成功
    if (img.empty()) {
        std::cerr << "Failed to load image\n";
        return 1;
    }

    // 将 8 位无符号数 CV_8U 转换为 64 位浮点数 CV_64F
    cv::Mat img_d;
    img.convertTo(img_d, CV_64F);

    // 3x3 Sobel 水平边缘检测算子
    cv::Mat kernel = (cv::Mat_<double>(3, 3) <<
        -1, -2, -1,
         0,  0,  0,
         1,  2,  1);

    cv::Mat manual_out;
    conv2d_manual(img_d, kernel, manual_out);

    cv::Mat opencv_out;
    cv::filter2D(img_d, opencv_out, CV_64F, kernel, cv::Point(-1, -1), 0, cv::BORDER_CONSTANT);

    // 裁剪 OpenCV 的输出，使其尺寸与手写输出一致
    cv::Mat opencv_cropped = opencv_out(cv::Rect(0, 0, manual_out.cols, manual_out.rows));

    // 计算两者的绝对差值
    cv::Mat diff;
    cv::absdiff(manual_out, opencv_cropped, diff);

    // 寻找差值矩阵中的最大值
    double max_diff;
    cv::minMaxLoc(diff, nullptr, &max_diff);

    std::cout << "Image size: " << img.cols << "x" << img.rows << "\n";
    std::cout << "Output size: " << manual_out.cols << "x" << manual_out.rows << "\n";
    std::cout << "Max difference (manual vs OpenCV): " << max_diff << "\n";

    if (max_diff < 1e-6) {
        std::cout << "PASS: outputs match\n";
    } else {
        std::cout << "FAIL: outputs differ\n";
    }

    // 将浮点结果转回 8 位用于显示（取绝对值，因为 Sobel 输出有负值）
    cv::Mat manual_show, opencv_show;
    cv::convertScaleAbs(manual_out, manual_show);
    cv::convertScaleAbs(opencv_cropped, opencv_show);

    cv::imshow("Original", img);
    cv::imshow("Manual Conv", manual_show);
    cv::imshow("OpenCV Conv", opencv_show);
    cv::waitKey(0);

    return 0;
}

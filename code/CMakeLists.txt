cmake_minimum_required(VERSION 3.10)
project(aricuic-learn)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(2d_convolution phase1/2d_convolution.cpp)
target_link_libraries(2d_convolution ${OpenCV_LIBS})

add_executable(im2col phase1/im2col.cpp)
target_link_libraries(im2col ${OpenCV_LIBS})

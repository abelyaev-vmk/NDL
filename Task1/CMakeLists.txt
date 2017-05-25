cmake_minimum_required(VERSION 3.5)
project(task1)
find_package( OpenCV REQUIRED )
set(CMAKE_CXX_STANDARD 11)

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

set(SOURCE_FILES main.cpp Clustering.h)
add_executable(task1 ${SOURCE_FILES})
target_link_libraries( task1 ${OpenCV_LIBS} )
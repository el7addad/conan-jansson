cmake_minimum_required(VERSION 3.8)

project(cmake_wrapper)

# Workaround for ${CMAKE_CURRENT_SOURCE_DIR} used in library's CMakeLists.txt
include(../conanbuildinfo.cmake)
conan_basic_setup(NO_OUTPUT_DIRS)

include("CMakeListsOriginal.txt")

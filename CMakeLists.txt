cmake_minimum_required(VERSION 2.8.11)

project(cmake_wrapper)

# Workaround for ${CMAKE_CURRENT_SOURCE_DIR} used in library's CMakeLists.txt
include(../conanbuildinfo.cmake)
conan_basic_setup(NO_OUTPUT_DIRS)

include("CMakeListsOriginal.txt")

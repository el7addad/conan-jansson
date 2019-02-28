#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    
    def configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os == "Macos" and self.settings.compiler == "gcc":
            cmake.definitions["CMAKE_C_COMPILER"] = "gcc-" + str(self.settings.compiler.version)
            cmake.definitions["CMAKE_CXX_COMPILER"] = "g++-" + str(self.settings.compiler.version)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin", "test_package")
            if self.settings.os == "Windows":
                self.run(bin_path)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path))
            else:
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path))

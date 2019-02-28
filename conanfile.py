#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class JanssonConan(ConanFile):
    name = "jansson"
    version = "2.11"
    url = "https://github.com/bincrafters/conan-jansson"
    homepage = "http://www.digip.org/jansson/"
    description = "C library for encoding, decoding and manipulating JSON data"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "use_urandom": [True, False],
        "use_windows_cryptoapi": [True, False]
    }
    default_options = ("shared=False", "fPIC=True", "use_urandom=True",
                       "use_windows_cryptoapi=True")
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        tools.get("{0}/releases/jansson-{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["JANSSON_BUILD_DOCS"] = False
        cmake.definitions["JANSSON_BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["JANSSON_EXAMPLES"] = False
        cmake.definitions["JANSSON_WITHOUT_TESTS"] = False
        cmake.definitions["USE_URANDOM"] = self.options.use_urandom
        cmake.definitions["USE_WINDOWS_CRYPTOAPI"] = self.options.use_windows_cryptoapi
        
        if self.settings.os == "Macos" and self.settings.compiler == "gcc":
            cmake.definitions["CMAKE_C_COMPILER"] = "gcc-" + str(self.settings.compiler.version)
            cmake.definitions["CMAKE_CXX_COMPILER"] = "g++-" + str(self.settings.compiler.version)

        if self.settings.compiler == "Visual Studio":
            if "MT" in self.settings.compiler.runtime:
                cmake.definitions["JANSSON_STATIC_CRT"] = True

        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class JanssonConan(ConanFile):
    name = "jansson"
    version = "2.11"
    url = "https://github.com/bincrafters/conan-jansson"
    description = "C library for encoding, decoding and manipulating JSON data"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
        "use_urandom": [True, False],
        "use_windows_cryptoapi": [True, False]}
    default_options = "shared=False", \
        "use_urandom=True", \
        "use_windows_cryptoapi=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        source_url = "http://www.digip.org/jansson"
        tools.get("{0}/releases/jansson-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)


    def build(self):
        cmake = CMake(self)

        cmake.definitions["JANSSON_BUILD_DOCS"] = False
        cmake.definitions["JANSSON_BUILD_SHARED_LIBS"] = True if self.options.shared else False
        cmake.definitions["JANSSON_EXAMPLES"] = False
        cmake.definitions["JANSSON_WITHOUT_TESTS"] = False
        cmake.definitions["USE_URANDOM"] = True if self.options.use_urandom else False
        cmake.definitions["USE_WINDOWS_CRYPTOAPI"] = True if self.options.use_windows_cryptoapi else False

        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                cmake.definitions["JANSSON_STATIC_CRT"] = True

        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        pass


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

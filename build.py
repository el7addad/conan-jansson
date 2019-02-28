#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default, build_shared
from cpt.packager import ConanMultiPackager


class FakeLinuxPlatformInfo(object):
    @staticmethod
    def system():
        return "Linux"


if __name__ == "__main__":

    if "GCC_ON_MACOS" in os.environ:
        builder = ConanMultiPackager(platform_info=FakeLinuxPlatformInfo())
        shared_option_name = None
        if build_shared.is_shared():
            shared_option_name = "%s:shared" % build_shared.get_name_from_recipe()
        builder.add_common_builds(shared_option_name=shared_option_name, pure_c=True, dll_with_static_runtime=False)
        filtered_builds = []
        for settings, options, env_vars, build_requires, reference in builder.items:
            settings["compiler.libcxx"] = "libstdc++"
            if not settings["arch"] == "x86":
                filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds
    else:
        builder = build_template_default.get_builder(pure_c=True)

    builder.run()
    

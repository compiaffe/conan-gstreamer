from conans import ConanFile, Meson, tools

import os

class GStreamerConan(ConanFile):
    name = "gstreamer"
    version = "master"
    url = "https://github.com/bincrafters/conan-" + name
    description = "A framework for streaming media"
    license = "https://gitlab.freedesktop.org/gstreamer/gstreamer/raw/master/COPYING"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        ("glib/2.58.1@bincrafters/stable"),
        ("bison/3.0.4@bincrafters/stable", "private"),
        ("flex/2.6.4@bincrafters/stable", "private")
    )

    def source(self):
        tools.get("https://github.com/GStreamer/gstreamer/archive/%s.tar.gz" % self.version)

    def build(self):
        args = ["--default-library=shared", "--libdir=lib", "-Dintrospection=disabled", "-Dexamples=disabled", "-Dtests=disabled"]
        meson = Meson(self)
        meson.configure(source_folder="gstreamer-" + self.version, args=args, pkg_config_paths=os.environ['PKG_CONFIG_PATH'].split(":"))
        meson.build()
        meson.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ["include/gstreamer-1.0"]
        self.env_info.PKG_CONFIG_PATH.append(os.path.join(self.package_folder, "lib", "pkgconfig"))
#!/usr/bin/env python

from distutils.core import setup, Extension
from distutils.command.install import install as _install


_VENDORED_RE2 = 're2-2016-05-01'


class InstallCommand(_install):
    boolean_options = _install.boolean_options + ['vendored-re2']
    user_options = _install.user_options + [
        ('vendored-re2', None, 'statically link against vendored re2'),
    ]

    def initialize_options(self):
        _install.initialize_options(self)
        self.vendored_re2 = False

    def run(self):
        if self.vendored_re2:
            import os
            import tempfile


            tmp_install_prefix = tempfile.mkdtemp()

            self.spawn([
                'make',
                '-C',
                _VENDORED_RE2,
                'install',
                'prefix=%s' % tmp_install_prefix,
                'CPPFLAGS=-fPIC',
            ])

            include_dirs = ['%s/include' % tmp_install_prefix]
            extra_objects = ['%s/lib/libre2.a' % tmp_install_prefix]

            ext_modules = [
                Extension('_re2',
                    sources = ['_re2.cc'],
                    include_dirs = include_dirs,
                    extra_objects = extra_objects,
                    extra_compile_args=['-std=c++11'],
                ),
            ]
        else:
            ext_modules = [
                Extension('_re2',
                    sources = ['_re2.cc'],
                    libraries = ['re2'],
                    extra_compile_args=['-std=c++11'],
                ),
            ]

        self.distribution.ext_modules = ext_modules

        return _install.run(self)


setup(
    cmdclass={
        'install': InstallCommand,
    },
    name="fb-re2",
    version="1.1.0",
    url="https://github.com/facebook/pyre2",
    description="Python wrapper for Google's RE2",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
    ],
    author="David Reiss",
    author_email="dreiss@fb.com",
    maintainer="Siddharth Agarwal",
    maintainer_email="sid0@fb.com",
    py_modules = ["re2"],
    )

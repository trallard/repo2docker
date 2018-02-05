"""Generates a Dockerfile based on an input matrix for Julia"""
import os
from .conda import CondaBuildPack


class JuliaBuildPack(CondaBuildPack):
    """
    Julia build pack which uses conda.

    The Julia build pack always uses the parent, `CondaBuildPack`,
    since Julia does not work with Python virtual environments.
    See https://github.com/JuliaPy/PyCall.jl/issues/410

    """
    def get_env(self):
        """Get additional environment settings for Julia and Jupyter

        Returns:
            an ordered list of environment setting tuples.
            The tuple contains a string of the environment variable name and
            a string of the environment setting. For example,
            `('JULIA_VERSION', '0.6.0')`

        """
        return super().get_env() + [
            ('JULIA_PATH', '${APP_BASE}/julia'),
            ('JULIA_HOME', '${JULIA_PATH}/bin'),
            ('JULIA_PKGDIR', '${JULIA_PATH}/pkg'),
            ('JULIA_VERSION', '0.6.0'),
            ('JUPYTER', '${NB_PYTHON_PREFIX}/bin/jupyter')
        ]

    def get_path(self):
        """Get path for Julia executables

         Returns:
             an ordered list of path strings. The path to the Julia
             executable is added to the list.

        """
        return super().get_path() + ['${JULIA_PATH}/bin']

    def get_build_scripts(self):
        return super().get_build_scripts() + [
            (
                "root",
                r"""
                mkdir -p ${JULIA_PATH} && \
                curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%[.-]*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" | tar -xz -C ${JULIA_PATH} --strip-components 1
                """
            ),
            (
                "root",
                r"""
                mkdir -p ${JULIA_PKGDIR} && \
                chown ${NB_USER}:${NB_USER} ${JULIA_PKGDIR}
                """
            ),
            (
                "${NB_USER}",
                # HACK: Can't seem to tell IJulia to install in sys-prefix
                # FIXME: Find way to get it to install under /srv and not $HOME?
                r"""
                julia -e 'Pkg.init(); Pkg.add("IJulia"); using IJulia;' && \
                mv ${HOME}/.local/share/jupyter/kernels/julia-0.6  ${NB_PYTHON_PREFIX}/share/jupyter/kernels/julia-0.6
                """
            )
        ]

    def get_assemble_scripts(self):
        require = self.binder_path('REQUIRE')
        return super().get_assemble_scripts() + [(
            "${NB_USER}",
            # Pre-compile all libraries if they've opted into it. `using {libraryname}` does the
            # right thing
            r"""
            cat "%(require)s" >> ${JULIA_PKGDIR}/v0.6/REQUIRE && \
            julia -e ' \
               Pkg.resolve(); \
               for pkg in keys(Pkg.Reqs.parse("%(require)s")) \
                pkg != "julia" && eval(:(using $(Symbol(pkg)))) \
               end \
            '
            """ % { "require" : require }
        )]

    def detect(self):
        return os.path.exists(self.binder_path('REQUIRE')) and super().detect()

# Make sure module environment is consistent regardless of whether
# we are working on a clean system or not!
if [[ -f /etc/bash.bashrc.local ]]; then
    . /etc/bash.bashrc.local
elif [[ -f /etc/profile.d/z00_modules.sh ]]; then
    . /etc/profile.d/z00_modules.sh 2> /dev/null

    if module --force purge >& /dev/null; then
        cray_module=$(module -t --show-hidden av crayenv |& tail -n1)

        if [[ -n $cray_module ]]; then
            module load $cray_module
        fi
    fi
fi

# If left set, will contaminate Spack child shells
unset BASH_ENV

# Initialize Bash Spack shell integration
. $NCAR_SPACK_STARTUP

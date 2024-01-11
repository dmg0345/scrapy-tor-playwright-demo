# syntax=docker/dockerfile:1
# escape=\

# Use latest Ubuntu available with Powershell and supported by Playwright.
FROM mcr.microsoft.com/powershell:7.3-ubuntu-jammy

# Ensure working from a known working directory.
WORKDIR "/"
# Ensure the active shell is PowerShell.
SHELL ["pwsh", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

# Update package sources, upgrade current installed packages and install new packages. For details refer to:
#   - https://packages.ubuntu.com/
#   - https://manpages.ubuntu.com/manpages/jammy/man8/apt-get.8.html
#   - https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ (apt-get)
#   - https://askubuntu.com/questions/875213/apt-get-to-retry-downloading (apt-get retries)
# It is possible that the Dockerfile breaks over time at this point as packages might be deprecated and not exist
# anymore when updates or upgrades are released, in this scenario, the package versions will need to be updated.
RUN 'Acquire::Retries "6";' > /etc/apt/apt.conf.d/80-retries;                                                          \
    apt-get --assume-yes update;                                                                                       \
    apt-get --assume-yes upgrade;                                                                                      \
    apt-get --assume-yes --show-progress install                                                                       \
    ## Python Packages #################################################################################################
    python3.11=3.11.0~rc1-1~22.04                                                                                      \
    python3.11-venv=3.11.0~rc1-1~22.04                                                                                 \
                                                                                                                       \
    ## Other ###########################################################################################################
    git=1:2.34.1-1ubuntu1.10;                                                                                          \
                                                                                                                       \
    apt-get --assume-yes clean;                                                                                        \
    apt-get --assume-yes autoremove;

# Create symbolic link from 'python3.11' to just 'python', and install 'pip' via bootstraped script to install 'poetry'.
RUN Push-Location "/usr/bin";                                                                                          \
    New-Item -ItemType SymbolicLink -Force -Path "/usr/bin/python" -Target "python3.11" | Out-Null;                    \
    Pop-Location;                                                                                                      \
    Invoke-WebRequest -UseBasicParsing -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "./get-pip.py";            \
    python get-pip.py "pip==23.3.2";                                                                                   \
    Remove-Item -Path "./get-pip.py" -Force;                                                                           \
    pip install --no-cache-dir poetry==1.3.2;

# Additional Git configurations, refer to:
#   - https://linuxhint.com/git-handle-symbolic-links/#3
#   - https://stackoverflow.com/questions/6842687/the-remote-end-hung-up-unexpectedly-while-git-cloning
#   - https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key#telling-git-about-your-ssh-key
# This forces the signing of all commits, user must provide 'user.name', 'user.email' and 'user.signingkey'.
RUN git config --global core.symlinks true;                                                                            \
    git config --global http.postBuffer 500M;                                                                          \
    git config --global http.maxRequestBuffer 100M;                                                                    \
    git config --global core.compression 0;                                                                            \
    git config --global gpg.format ssh;                                                                                \
    git config --global commit.gpgsign true;

## Virtual Environments Configuration ##################################################################################
# Set the path where virtual environments will be created.
ENV VIRTUAL_ENVS_DIR="/usr/venvs"

# Copy 'pyproject.toml' file and 'poetry.lock' file, if it exists, to the virtual environment directory.
COPY "../pyproject.toml" "${VIRTUAL_ENVS_DIR}/pyproject.toml"
COPY "../poetry.[l]ock" "${VIRTUAL_ENVS_DIR}/poetry.lock"

## Create 'development' virtual environment
# Set the name and location of the 'development' virtual environment as environment variables.
ENV VIRTUAL_ENVS_DEVELOPMENT_NAME="development"
ENV VIRTUAL_ENVS_DEVELOPMENT_DIR="${VIRTUAL_ENVS_DIR}/${VIRTUAL_ENVS_DEVELOPMENT_NAME}"

# Create the virtual environment, activate it and:
#   - Install 'production' and 'development' dependencies with Poetry.
#   - Use 'nodeenv' to install 'nodejs' along with 'npm' within the Python environment.
#   - Use 'npm' to install 'pyright' globally within the environment.
#   - Install playwright Chromium browser.
#   - Erase caches to decrease size of the image.
RUN Push-Location $env:VIRTUAL_ENVS_DIR;                                                                               \
    python -m venv $env:VIRTUAL_ENVS_DEVELOPMENT_NAME;                                                                 \
    & $env:VIRTUAL_ENVS_DEVELOPMENT_DIR/bin/Activate.ps1;                                                              \
    poetry install --only main,dev --no-cache --no-interaction;                                                        \
    nodeenv --python-virtualenv --node 20.3.1 --npm 9.6.7;                                                             \
    npm install --global pyright@1.1.316;                                                                              \
    python -m playwright install chromium --with-deps;                                                                 \
    npm cache clean --force;                                                                                           \
    Remove-Item ~/.cache/pypoetry -Force -Recurse;                                                                     \
    deactivate;                                                                                                        \
    Pop-Location;

## Create 'production' virtual environment
# Set the name and location of the 'production' virtual environment as environment variables.
ENV VIRTUAL_ENVS_PRODUCTION_NAME="production"
ENV VIRTUAL_ENVS_PRODUCTION_DIR="${VIRTUAL_ENVS_DIR}/${VIRTUAL_ENVS_PRODUCTION_NAME}"

# Create the virtual environment, activate it and:
#   - Install 'production' dependencies with Poetry.
#   - Use 'nodeenv' to install 'nodejs' along with 'npm' within the Python environment.
#   - Install playwright Chromium browser.
#   - Erase caches to decrease size of the image.
RUN Push-Location $env:VIRTUAL_ENVS_DIR;                                                                               \
    python -m venv $env:VIRTUAL_ENVS_PRODUCTION_NAME;                                                                  \
    & $env:VIRTUAL_ENVS_PRODUCTION_DIR/bin/Activate.ps1;                                                               \
    poetry install --only main --no-cache --no-interaction;                                                            \
    nodeenv --python-virtualenv --node 20.3.1 --npm 9.6.7;                                                             \
    python -m playwright install chromium --with-deps;                                                                 \
    npm cache clean --force;                                                                                           \
    Remove-Item ~/.cache/pypoetry -Force -Recurse;                                                                     \
    deactivate;                                                                                                        \
    Pop-Location;

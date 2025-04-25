# My Dev Tools

## Vim config

Since I have to use both Microsoft Windows & Linux and want to use the same VIM settings,
I have structured the files as follows.

Remove the dot prefix from vim files to avoid the Microsoft's poor handling of dot file 
and place all vim configuration files into a folder.

### On Windows

Put the "\_vimrc" in the %HOME% directory. Sometimes %HOME% is on a remote share, so \_vimrc 
redefines HOME to be %USERPROFILE% which is local. \_vimrc then sets VIMFILES to be the folder 
vimfiles in the %USERPROFILE% folder.

Copy all files in the repo vimfiles folder into the vimfiles folder in %USERPROFILE% folder.

### On Linux

Put the "\.vimrc" in the Home directory. It then sources the vimrc file in .vim folder.

Copy all files in the repo vimfiles folder into the .vim folder in Home.

## Global

A gtags.conf file

## build_shell

### Build and install

python version.py will print out the version number i.e. $pkgver

To build and install follow PEP517...

Install the python packages "pip", "setuptools", "wheel" and "build".

To build the package...

python -m build

pip install dist/build_shell-$pkgver-py3-none-any.whl


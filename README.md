my_vim
======

My Vim config

Since I have to use both Microsoft Windows & Linux and want to use the same VIM settings,
I have structured the files as follows.

Remove the dot prefix from vim files to avoid the Microsoft's poor handling of dot file 
and place all vim configuration files into a folder.

On Windows
-----------

Put the "\_vimrc" in the %HOME% directory. Sometimes %HOME% is on a remote share, so \_vimrc 
redefines HOME to be %USERPROFILE% which is local. \_vimrc then sets VIMFILES to be the folder 
vimfiles in the %USERPROFILE% folder.

Copy all files in the repo vimfiles folder into the vimfiles folder in %USERPROFILE% folder.

On Linux
---------

Put the "\.vimrc" in the Home directory. It then sources the vimrc file in .vim folder.

Copy all files in the repo vimfiles folder into the .vim folder in Home.

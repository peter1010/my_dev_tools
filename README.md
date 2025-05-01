# My Dev Tools

## build_shell

### Summary

A Tkinter application that is a wrapper around calling make, cargo, ninja or ghs. It captures the output, parses it and highlights
warnings in yellow and error is red. Selecting a hightlighted line will open vim to edit the code associated with the warning.

### Run

Run the code from within your build environment like so...

> python /path/build_shell

where path is the path to the build_shell folder.

It will search for a "makefile", "Cargo.toml", "ninja.build" or "default.gpj"

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



" In Windows sometimes the HOME directory is defined as a remote drive
" Lets make it local (also get rid of the dots)
" Note it is not possble to change the value of MYVIMRC
" Lets make HOME be local (also get rid of the dots)
" Note $GVIMRC => $VIMFILE/gvimrc
"
let $HOME = $USERPROFILE
let $VIMFILES = '~/vimfiles'
set runtimepath=$VIMFILES,$VIMRUNTIME
source $VIMFILES/vimrc
set viminfo+=n$USERPROFILE/vimfiles/viminfo

if exists("b:my_ftplugin")
  finish
endif

let b:my_ftplugin = 1
call DetectIndentation("python")

" Stop indentation being change by standard python.vim file
let g:python_recommended_style = 0

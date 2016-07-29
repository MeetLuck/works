"session restore
"so ~/last.vis
"rv! ~/last.info
set nocompatible
"source $VIMRUNTIME/vimrc_example.vim
"source $VIMRUNTIME/mswin.vim
" behave mswin : <C-a> <C-c> <C-v>
"

"---> Pathogen setting
"cp pathogen.vim ~/.vim/autoload
"filetype off
"execute pathogen#infect()
"<---- end of Pathogen

"----> vundle setting 
filetype off
set rtp +=~/.vim
set rtp +=~/.vim/bundle/Vundle.vim
" cd %HOME%/.vim/bundle/Vundle.vim/  where %HOME% = K:/program/home
" git clone https://github.com/VundleVim/Vundle.vim.git .
call vundle#begin('~/.vim/bundle')
Plugin 'VundleVim/Vundle.vim'
Plugin 'pprovost/vim-ps1'
Plugin 'moll/vim-node'
Plugin 'altercation/vim-colors-solarized'
Plugin 'jnurmine/Zenburn'
Plugin 'scrooloose/syntastic'
"Plugin 'nvie/vim-flake8'
call vundle#end()


"Plugin 'vimwiki/vimwiki'
"Plugin 'tomtom/viki_vim'
"let g:pydiction_location = '~/.vim/bundle/pydiction/complete-dict'
"<---- vundle setting end:q


set nobackup
set autowrite
set ts=4 sw=4 sts=4 et
set laststatus =2 
set guifont=Anonymous_Pro:h11
syntax on
let python_hightlight_all = 1
filetype plugin indent on
set hidden

"colorscheme solarized
if has("gui_running")
    set background=dark
    colorscheme solarized
else
    colorscheme zenburn
endif

" start runs program with seperate process
nnoremap <silent> <F5> :!start cmd /c python % & pause<CR>
"if has("autocmd")
"    autocmd FileType ruby,html,text,css setlocal ts=2 sts=2 sw=2 expandtab
"    autocmd User Node if &filetype == "javascript" | setlocal
"    autocmd FileType html iab <p <p></p>
"    autocmd FileType html iab <b <b></b>
"    autocmd FileType html iab <e <em></em>
"    autocmd FileType html iab <h <h3></h3>
"    autocmd FileType html iab <m <mark></mark>
"    autocmd FileType html iab <mark1> <mark id='mark1'></mark>
"    autocmd FileType html iab <tr> <tr></tr>
"    autocmd FileType html iab <td> <td></td>
"    autocmd FileType html iab <th> <th></th>
"    autocmd FileType html iab <divEx> <div class="Ex"><cr></div>
"    autocmd FileType html iab <table> <table class="tipf"><cr></table>
"endif
"--> :help syntastic
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
"<-- end systastic

set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

highlight Cursor guifg=white guibg=darkgreen
highlight iCursor guibg=green
set guicursor=i:ver35-iCursor
hi User1 guifg=darkgreen guibg=black
hi User2 guifg=darkorange guibg=black
set statusline=
set statusline+=%2*[%n]                      "buffernr
set statusline+=%1*\ %<%F               "File+path modified readonly
set statusline+=%2*\%m%r%h\ %9y\                     "FileType
set statusline+=%=
set statusline+=%2*\%2cc\ "Column
set statusline+=%1*\ %l/%L(%p%%)\  "Rownumber/total (%)
"FileWritePre* :call strftime('%c')
"function! DateInsert()
"    $r !date /T
"endfunction
""autocmd FileWritePre *  strftime("%c")
"autocmd FileWritePre * :call DateInsert()

#!/usr/bin/perl

$pdf_mode = 4;
$out_dir = 'build';
$pdf_previewer = 'open -a Skim';

@generated_exts = (@generated_exts, 'synctex.gz');
@default_files = (
  'main.tex', 
  'construction.tex', 
  './K-construction-2.tex',
  './K-construction-3.tex',
);

set_tex_cmds('--shell-escape -synctex=1 -interaction=nonstopmode %O %S');

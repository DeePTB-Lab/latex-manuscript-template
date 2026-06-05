$bibtex_use = 2;
$interaction = 'nonstopmode';
$halt_on_error = 1;

$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode -halt-on-error %O %S';
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -halt-on-error %O %S';
$lualatex = 'lualatex -synctex=1 -interaction=nonstopmode -halt-on-error %O %S';

$clean_ext .= ' synctex.gz run.xml bcf';

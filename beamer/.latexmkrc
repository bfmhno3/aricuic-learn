# 主文件
$root = 'main.tex';

# 输出目录
$out_dir = 'build';
$aux_dir = 'build';

# 编译引擎: XeLaTeX
$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';

# 自动运行 BibTeX 或 Biber
$bibtex_use = 2;

# 清理时保留 PDF
$clean_ext = 'aux bbl bcf blg fdb_latexmk fls log out run.xml synctex.gz toc';

# 跨平台 PDF 预览器
if ($^O eq 'MSWin32') {
    $pdf_previewer = 'start %S';
} elsif ($^O eq 'darwin') {
    $pdf_previewer = 'open %S';
} else {
    $pdf_previewer = 'xdg-open %S 2>/dev/null || evince %S';
}

# Windows 下清理时不删除被占用的文件
if ($^O eq 'MSWin32') {
    $cleanup_includes_generated = 0;
}

# 自定义依赖示例（取消注释即可用）
# add_cus_dep('glo', 'gls', 0, 'makeglos');
# sub makeglos {
#     system("makeindex -s $_[0].ist -t $_[0].glg -o $_[0].gls $_[0].glo");
# }
# AITEC Survey
anaconda https://www.continuum.io/downloads
launch anaconda navigator, run upgrades
launch anaconda prompt
conda install plotly
conda install entrypoints

jupyter notebook
edit in browser
save

jupyter nbconvert --to slides --template mytemplate.tpl --reveal-prefix reveal.js "AITEC Slideshow.ipynb"
jupyter nbconvert --to html --template mytemplate.tpl "AITEC Slideshow.ipynb"

(print html to pdf)


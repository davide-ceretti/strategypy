# Uses https://github.com/benqus/strategypy-ui and expect it to be cloned in ../
rm -rf ../strategypy-ui/example.json
./play.sh > ../strategypy-ui/example.json
firefox ../strategypy-ui/index.html

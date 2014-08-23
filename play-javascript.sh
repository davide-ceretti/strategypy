# Uses https://github.com/benqus/strategypy-ui and expect it to be cloned in ../
mv ../strategypy-ui/example.json ../strategypy-ui/example.json.old
./play.sh > ../strategypy-ui/example.json
firefox ../strategypy-ui/index.html
mv ../strategypy-ui/example.json.old ../strategypy-ui/example.json

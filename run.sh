python3 enumerate.py | parallel -j 8 python3 main.py --level cd116 {}
python3 enumerate.py | parallel -j 8 python3 main.py --level block {}
python3 enumerate.py | parallel -j 8 python3 main.py --level bg {}
python3 enumerate.py | parallel -j 8 python3 main.py --level vtd {}
python3 enumerate.py | parallel -j 8 python3 main.py --level tract {}
python3 enumerate.py | parallel -j 8 python3 main.py --level county {}
python3 enumerate.py | parallel -j 8 python3 main.py --level place {}
python3 enumerate.py | parallel -j 8 python3 main.py --level cousub {}
python3 enumerate.py | parallel -j 8 python3 main.py --level sldu {}
python3 enumerate.py | parallel -j 8 python3 main.py --level sldl {}


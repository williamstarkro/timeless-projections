env:
	virtualenv --python=python3 env

setup: env requirements.txt
	. env/bin/activate && pip3 install -r requirements.txt

notebook:
	. env/bin/activate && jupyter notebook



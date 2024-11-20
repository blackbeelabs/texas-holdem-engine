make local:
	pip install loguru==0.7.2
	
make pytest:
	pytest

make local_notebook:
	pip install notebook==6.4.13
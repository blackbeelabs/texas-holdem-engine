PYTHON_VERSION := 3.11.1
make local:
	pip install loguru==0.7.2 # As of 1 Jan 2024
	
make pytest:
	pip install pytest==8.2.2 # As of 1 Jul 2024

make local_notebook:
	pip install notebook==6.5.4 # Freeze this version
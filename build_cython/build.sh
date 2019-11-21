# !/bin/bash
mv ../ctools ./
python setup.py build_ext --inplace
rm ./ctools/ccctest.cpp
rm -rf ./build
mv ctools ../

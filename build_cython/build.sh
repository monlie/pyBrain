!/bin/bash
mv ../ctools ./
python setup.py build_ext --inplace -c mingw32

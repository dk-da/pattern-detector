패턴디텍터입니다.

$ python run.py를 실행하면 training.json 안의 뉴스기사안에서 POI name을 추출합니다.

사용하기위해서는 mecab-ko, mecab-ko-dic, mecab-python 랩퍼를 설치해야합니다.

(refs: https://bitbucket.org/eunjeon/mecab-ko-dic)


1) mecab-ko 설치방법

$ wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.1.tar.gz

$ tar zxvf mecab-0.996-ko-0.9.1.tar.gz

$ cd mecab-0.996-ko-0.9.1

$ ./configure

$ make

$ make check

$ su

$ sudo make install


2) mecab-ko-dic 설치방법

$ wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-1.6.1-20140814.tar.gz

$ tar zxvf mecab-ko-dic-1.6.1-20140814.tar.gz

$ cd mecab-ko-dic-1.6.1-20140814

$ ./configure

$ make

$ su

$ sudo make install

에러날경우
$ sudo ldconfig
를 한뒤에 재시도


3) mecab python wrapper 설치방법

$ wget https://mecab.googlecode.com/files/mecab-python-0.996.tar.gz

$ tar zxvf mecab-python-0.996.tar.gz

$ cd mecab-python-0.996

$ python setup.py build

$ sudo python setup.py install


You can change the install directory with the --prefix option. For example:
$ python setup.py install --prefix=/tmp/pybuild/foobar



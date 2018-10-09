# Mcoin
```
(0) 開port
  4001
  5000
  5001


(1) 安裝套件
  python3.6
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install -y python3.6
    sudo rm /usr/bin/python3
    sudo ln -s /usr/bin/python3.6 /usr/bin/python3
    sudo apt-get -qqy install python3.6-dev
    sudo apt -qqy install python3-setuptools
    sudo apt-get install -y gcc
    sudo easy_install3 pip
    sudo add-apt-repository ppa:ethereum/ethereum
    sudo apt-get update
    sudo apt-get -qqy install solc
  
  pyethereum
    sudo apt-get install libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev libyaml-cpp-dev
    git clone https://github.com/ethereum/pyethereum/
    cd pyethereum
    sudo python3 setup.py install
    
  pip3 install
    web3
    flask
    flask-cors
    py-solc
    ipfsapi

  ipfs
    wget https://dist.ipfs.io/go-ipfs/v0.4.17/go-ipfs_v0.4.17_linux-amd64.tar.gz
    tar xvfz go-ipfs_v0.4.17_linux-amd64.tar.gz
    sudo mv go-ipfs/ipfs /usr/local/bin/ipfs


(2) 改參數
  find . -type f -print0 | xargs -0 sed -i 's///g'
    erc20 address
    super address
    password of super user
  mcoin.conf


(3) 啟動
  ipfs
  api


(4) User合約
    第一台執行deploy
    第n台後複製users.json


(5) ipfs connect所有節點
```

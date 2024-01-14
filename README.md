# BattleShip Game

Battleship is a strategic game where you engage in combat against the computer.

## Description

The game is developed using the Python Arcade library, featuring graphics composed of textured geometric shapes that enhance the visual experience. Player control is intuitive, driven by mouse input, providing an easy-to-use interface. Players have the option to select from three difficulty levels.

In the easy difficulty setting, enemy shots are distributed randomly across the game board, creating an unpredictable challenge. On the normal difficulty level, a more sophisticated strategy is employed. If an enemy hits your ship, the subsequent shot will be directed around the impacted area. This allows the enemy to determine the orientation of your ship before proceeding to systematically target and destroy it. The hard difficulty is an upgraded version of normal difficulty, where, if a shot misses the boat, the enemy will change the target location for the next shot.

With engaging gameplay and varying difficulty levels, the game offers a dynamic and strategic experience for players of all skill levels.

## How to play
The objective of the game is to locate all enemy ships hidden behind clouds and destroy them before the enemy annihilates all your ships.
<ol>
  <li>Select difficulty level.</li>
  <li>Place your ships on your game board (you can rotate ships by pressing `R` or the `Right mouse button`).</li>
  <li>When it's your turn, click on a cloud on the enemy's game board and attempt to hit a ship.</li>
  <li>Destroy the enemy's ships before all of your ships are destroyed.</li>
</ol>


## Requirements

Python version 3.12.1<br>
Python Arcade library version 3.0.0dev25<br><br>
You may need additional dependencies for installing Python or ensuring the proper functioning of the Arcade library such as:
<ul>
  <li>build-essential</li>
  <li>zlib1g-dev</li>
  <li>libssl-dev</li>
  <li>libbz2-dev</li>
  <li>libreadline-dev</li>
  <li>libsqlite3-dev</li>
  <li>llvm</li>
  <li>libncurses5-dev</li>
  <li>libncursesw5-dev</li>
  <li>xz-utils</li>
  <li>tk-dev</li>
  <li>libffi-dev</li>
  <li>liblzma-dev</li>
  <li>python3-openssl</li>
</ul>

## Instalation on Debian

Instalation dependencies:
```
apt install -y build-essential zlib1g-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
```

Download Python 3.12.1: 
```
wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz
```
Extract and install Python:
```
tar -xf Python-3.12.1.tgz
cd Python-3.12.1
./configure
make
sudo make install
```
Add Python to PATH:
```
export PATH=/usr/local/bin:$PATH
ln -s /usr/local/bin/python3.12 /usr/local/bin/python
```
Install Arcade library via pip:
```
pip install arcade==3.0.0dev25
```
in some cases use:
```
pip3 install arcade==3.0.0dev25
```

## Instalation on Mac
On Mac you can use pre-installed Python and almost all dependencies should be installed except for 'jpeg'. If the game doesn't run correctly, you may try installing a newer version of Python.<br>
To install dependencies it's recomended to have installed <a href=brew.sh>Homebrew</a>.<br>
Instalation of dependencies:
```
brew install jpeg
```
Adding jpeg to PATH:
```
export PATH="/opt/homebrew/opt/jpeg/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/jpeg/lib"
export CPPFLAGS="-I/opt/homebrew/opt/jpeg/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/jpeg/lib/pkgconfig"
```
Install Arcade library via pip:
```
pip install arcade==3.0.0dev25
```
in some cases use:
```
pip3 install arcade==3.0.0dev25
```

## Run

Run file 'main.py':
```
python main.py
```
or
```
python3 main.py
```
sudo apt update
sudo apt install -y git
sudo apt install -y python3-pip
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install aiohttp
git clone https://github.com/hamonangann/thesis
cd thesis
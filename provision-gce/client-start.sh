sudo apt update
sudo apt install -y git
sudo apt install -y python3-pip
python -m venv venv
source venv/bin/activate
pip3 install aiohttp
git clone https://github.com/hamonangann/thesis
cd thesis
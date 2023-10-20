sudo apt install unzip
curl —fsSL https://bun.sh/install.sh | bash # install bun, its like npm but better
source /root/.bashrc 
bun install # install all dependencies
# for some reason bun install doesn't install fontawesome
bun i --save @fortawesome/fontawesome-svg-core
bun install --save @fortawesome/free-solid-svg-icons
bun install --save @fortawesome/react-fontawesome
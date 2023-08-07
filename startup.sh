#!/bin/bash

# Function to modify the config.yml file with random values for py_port and gui_port
modify_config_file() {
    py_port=$(shuf -i 9000-9999 -n 1)
    gui_port=$(shuf -i 9000-9999 -n 1)

    sed -i "s/py_port: [0-9]*/py_port: $py_port/" config.yml
    sed -i "s/gui_port: [0-9]*/gui_port: $gui_port/" config.yml
}

run_python3() {
    conda activate hrip
    python3 main.py
    conda deactivate
}

run_backend() {
    conda activate hrip
    python3 manage.py runserver
    conda deactivate
}

run_vision() {
    python main.py
}

run_python2() {
    python main.py
}


# Main execution order

modify_config_file

cd python3
run_python3 &
cd ..

cd backend
run_backend &
cd ..

cd vision
run_vision &
cd ..

sleep 10

cd python2
run_python2 &
cd ..


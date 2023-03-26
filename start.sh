#!/bin/bash
echo "Bem vindo pai, rodarei seus comandos:"

kill -9 $(sudo lsof -t -i:210)

gnome-terminal --tab --title "Server" -- bash -c "python3 server.py; exec bash -i"

gnome-terminal --tab --title "Client" -- bash -c "python3 client.py; exec bash -i"

gnome-terminal --tab --title "Client" -- bash -c "python3 client.py; exec bash -i"


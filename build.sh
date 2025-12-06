#!/bin/bash

source .venv/bin/activate
pip install --upgrade pip 
pip install -r requirements.txt
reflex init 
if [ -f "frontend.zip" ]; then
    rm frontend.zip
fi
if [ -d "public" ]; then
    rm -rf public
fi
reflex export --frontend-only  
unzip frontend.zip -d public
if [ -f "frontend.zip" ]; then
    rm frontend.zip
fi 
deactivate

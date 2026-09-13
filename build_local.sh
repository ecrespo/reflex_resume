#!/bin/bash
set -e

uv sync --frozen
uv run reflex init
if [ -f "frontend.zip" ]; then
    rm frontend.zip
fi
if [ -d "public" ]; then
    rm -rf public
fi
uv run reflex export --frontend-only
unzip frontend.zip -d public
if [ -f "frontend.zip" ]; then
    rm frontend.zip
fi

#!/usr/bin/env bash
jupyter nbconvert --to html notebooks/$(ls notebooks | head -n1) --output docs/index.html

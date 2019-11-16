#!/bin/sh
echo "Symbols that are most often repeated"
ls data/ | sed 's/\..*$//g' | sort | uniq -c | sort -n | tail -n 10

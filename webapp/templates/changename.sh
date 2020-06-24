#!/bin/bash
cd $1
rm -rf ../static/
mv assets/ ../static/
mkdir ../static/uploads
sed -i'.bs' -e 's|assets/|static/|g' *.html
rm -f *.html.bs

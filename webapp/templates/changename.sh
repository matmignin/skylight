#!/bin/bash
cd $1
mv ../static/uploads assets/uploads/
rm -rf ../static/
mv assets/ ../static/
#mkdir ../static/uploads
#mkdir ../static/uploads/mat
#mkdir ../static/uploads/mike
#mkdir ../static/uploads/tony
#mkdir ../static/uploads/christie
#mkdir ../static/uploads/que 
sed -i'.bs' -e 's|assets/|static/|g' *.html
rm -f *.html.bs

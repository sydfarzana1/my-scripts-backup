#!/bin/bash

echo "Enter name of file:"
read -r file

# Build full path once
filepath="$(pwd)/$file.sh"

# Create and make executable
touch "$filepath"
chmod +x "$filepath"

# Write template
echo '#!/bin/bash' >> "$filepath"
echo "#SCRIPT : $(basename "$filepath")" >> "$filepath"
echo '#AUTHOR : ASIYA FARZANA SYEDA' >> "$filepath"
echo '#PURPOSE:' >> "$filepath"
echo "#DATE   : $(date)" >> "$filepath"
echo '#############################################################' >> "$filepath"
echo '####################PROGRAM STARTS HERE######################' >> "$filepath"
echo '#############################################################' >> "$filepath"

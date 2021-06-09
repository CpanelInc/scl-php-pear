#!/bin/bash

source debian/vars.sh

set -x

# Create a usable PEAR directory (used by install-pear.php)
for archive in debian/SOURCES_FROM_SPEC/*.tgz
do
    tar xf $archive --strip-components 1 || tar xf $archive --strip-path 1
    file=${archive##*/}
    [ -f LICENSE ] && mv LICENSE LICENSE-${file%%-*}
    [ -f README ]  && mv README  README-${file%%-*}
    tar -xf $archive --wildcards 'package*xml'
    [ -f package2.xml ] && mv package2.xml ${file%%-*}.xml \
                        || mv package.xml  ${file%%-*}.xml
done
cp $SOURCE1 .
cp $SOURCE30 sanity_check.sh
chmod a+x sanity_check.sh


#!/bin/bash

source debian/vars.sh

set -x

mkdir -p $DEB_INSTALL_ROOT/

export phpbin=/opt/cpanel/$scl_name/root/usr/bin/php

rm -rf $DEB_INSTALL_ROOT
export PHP_PEAR_SYSCONF_DIR=$_sysconfdir
export PHP_PEAR_SIG_KEYDIR=$_sysconfdir/pearkeys
export PHP_PEAR_SIG_BIN=$_root_bindir/gpg
export PHP_PEAR_INSTALL_DIR=$peardir
# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}$_localstatedir/cache/php-pear
# We fix this in post, and update the 'temp_dir' setting
# to use _localstatedir/tmp/php-pear instead.
export PHP_PEAR_TEMP_DIR=/var/tmp
install -d $DEB_INSTALL_ROOT$peardir \
           $DEB_INSTALL_ROOT$_bindir \
           $DEB_INSTALL_ROOT$_localstatedir/cache/php-pear \
           $DEB_INSTALL_ROOT$_localstatedir/tmp/php-pear \
           $DEB_INSTALL_ROOT$_localstatedir/www/html \
           $DEB_INSTALL_ROOT$metadir/pkgxml \
           $DEB_INSTALL_ROOT$_docdir/pecl \
           $DEB_INSTALL_ROOT$_datadir/tests/pecl \
           $DEB_INSTALL_ROOT$_sysconfdir/pear \
           $DEB_INSTALL_ROOT$_sysconfdir/php.d
export INSTALL_ROOT=$DEB_INSTALL_ROOT
pwd
$phpbin --version
$phpbin -dmemory_limit=64M -dshort_open_tag=0 -dsafe_mode=0 \
         -d 'error_reporting=E_ALL&~E_DEPRECATED' -ddetect_unicode=0 \
         install-pear.php --force \
                 --dir      $peardir \
                 --cache    $_localstatedir/cache/php-pear \
                 --download $_localstatedir/tmp/php-pear/cache \
                 --config   $_sysconfdir/pear \
                 --bin      $_bindir \
                 --www      $_localstatedir/www/html \
                 --doc      $_docdir/pear \
                 --test     $_datadir/tests/pear \
                 --data     $_datadir/pear-data \
                 --metadata $metadir \
                 *.tgz
install -m 755 $SOURCE10 $DEB_INSTALL_ROOT$_bindir/pear
# Set up autoconf and autoheader for PHP73 and C6 use
install -m 755 $SOURCE11 $DEB_INSTALL_ROOT$_bindir/pecl
install -m 755 $SOURCE12 $DEB_INSTALL_ROOT$_bindir/peardev
# Create symlinks to /usr/bin/ea-php##-pear
install -d $DEB_INSTALL_ROOT/usr/bin
ln -sf $_bindir/pear $DEB_INSTALL_ROOT/usr/bin/$scl-pear
ln -sf $_bindir/pecl $DEB_INSTALL_ROOT/usr/bin/$scl-pecl
# Need to touch pecl.ini so it can write to it
touch $DEB_INSTALL_ROOT$_sysconfdir/php.d/zzzzzzz-pecl.ini
# Fix path in SCL
for exe in pear pecl peardev; do
    sed -e 's: /usr: $_prefix:' \
        -i $DEB_INSTALL_ROOT$_bindir/$exe
done
# Sanitize the pear.conf
$phpbin $SOURCE3 $DEB_INSTALL_ROOT$_sysconfdir/pear.conf ext_dir >new-pear.conf
$phpbin $SOURCE3 new-pear.conf http_proxy > $DEB_INSTALL_ROOT$_sysconfdir/pear.conf
$phpbin -r "print_r(unserialize(substr(file_get_contents('$DEB_INSTALL_ROOT$_sysconfdir/pear.conf'),17)));"
# Why this file here ?
rm -rf $DEB_INSTALL_ROOT/.depdb* $DEB_INSTALL_ROOT/.lock $DEB_INSTALL_ROOT/.channels $DEB_INSTALL_ROOT/.filemap
# Need for re-registrying XML_Util
install -m 644 *.xml $DEB_INSTALL_ROOT$metadir/pkgxml

# Move the files where the install file thinks they should be

mkdir -p ./debian/tmp/usr/share/doc/$scl_name-pear-$version
mkdir -p ./debian/tmp/usr/share/licenses/$scl_name-pear-$version
mkdir -p ./debian/tmp/var/cache/php-pear
mkdir -p ./debian/tmp/var/tmp/php-pear

cp -n ./debian/tmp/usr/share/doc/pear/PEAR/README.rst ./debian/tmp/usr/share/doc/$scl_name-pear-$version/README.rst
cp -n ./LICENSE* ./debian/tmp/usr/share/licenses/$scl_name-pear-$version



echo "FILELIST"
find . -type f -print


#!/bin/sh

# C6 and PHP73 need newer auto(conf|header) so we need to set our own
export PHP_AUTOCONF=/opt/rh/autotools-latest/root/usr/bin/autoconf
export PHP_AUTOHEADER=/opt/rh/autotools-latest/root/usr/bin/autoheader

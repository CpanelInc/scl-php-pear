#!/bin/sh

RPM_BUILD_ROOT=$1
SYSCONFDIR=$2
LIBDIR=$3

grep ${RPM_BUILD_ROOT} ${RPM_BUILD_ROOT}${SYSCONFDIR}/pear.conf && exit 1
grep ${LIBDIR} ${RPM_BUILD_ROOT}${SYSCONFDIR}/pear.conf && exit 1
grep '"/tmp"' ${RPM_BUILD_ROOT}${SYSCONFDIR}/pear.conf && exit 1
grep /usr/local ${RPM_BUILD_ROOT}${SYSCONFDIR}/pear.conf && exit 1
grep -rl $RPM_BUILD_ROOT $RPM_BUILD_ROOT && exit 1

exit 0

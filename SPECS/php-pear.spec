%define debug_package %{nil}

%{?scl:%global _scl_prefix /opt/cpanel}
%{?scl:%scl_package %{scl}-pear}
%{?scl:BuildRequires: scl-utils-build}
%{?scl:Requires: %scl_runtime}
%{!?scl:%global pkg_name %{name}}

# must redefine this in the spec file because OBS doesn't know how
# to handle macros in BuildRequires statements
%{?scl:%global scl_prefix %{scl}-}

# Reference: rh-php56-php-pear-1.9.5-3.el7.centos.src.rpm

%global pkg_name         %{name}
%global _root_sysconfdir %{_sysconfdir}
%global metadir          %{_localstatedir}/lib/pear
%global peardir          %{_datadir}/pear

Summary: PHP Extension and Application Repository framework
Name: %{?scl}-pear
Version: 1.10.1
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4568 for more details
%define release_prefix 10
Release: %{release_prefix}%{?dist}.cpanel

# PEAR, Archive_Tar, XML_Util are BSD
# Console_Getopt is PHP
# Structures_Graph is LGPLv2+
License: BSD and PHP and LGPLv2+
Group: Development/Languages
URL: http://pear.php.net/package/PEAR
Vendor: cPanel, Inc.
Source0: PEAR-1.10.1.tgz
# wget https://raw.github.com/pear/pear-core/master/install-pear.php
Source1: install-pear.php
Source3: strip.php

# Simpler scripts to place in bindir
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh

Source21: Archive_Tar-1.4.3.tgz
Source22: Console_Getopt-1.4.1.tgz
Source23: Structures_Graph-1.1.1.tgz
Source24: XML_Util-1.3.0.tgz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-cli
BuildRequires: %{?scl_prefix}php-xml
BuildRequires: gnupg

# phpci detected extension
# PEAR (date, spl always builtin):
Requires:  %{?scl_prefix}php-cli
Requires:  %{?scl_prefix}php-ftp
Requires:  %{?scl_prefix}php-tokenizer
Requires:  %{?scl_prefix}php-xml

# XML_Util: pcre
# Console_Getopt: pcre
# Archive_Tar: pcre, posix, zlib
# Structures_Graph: none
# most pecl invocations need php-devel
Requires:  %{?scl_prefix}php-pcre
Requires:  %{?scl_prefix}php-posix
Requires:  %{?scl_prefix}php-zlib
Requires:  %{?scl_prefix}php-devel

Provides:  %{?scl_prefix}php-pear(Console_Getopt) = 1.4.1
Provides:  %{?scl_prefix}php-pear(Archive_Tar) = 1.4.3
Provides:  %{?scl_prefix}php-pear(PEAR) = 1.10.1
Provides:  %{?scl_prefix}php-pear(Structures_Graph) = 1.1.1
Provides:  %{?scl_prefix}php-pear(XML_Util) = 1.3.0

%description
PEAR/PECL is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cT

# Create a usable PEAR directory (used by install-pear.php)
for archive in %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}
do
    tar xzf  $archive --strip-components 1 || tar xzf  $archive --strip-path 1
    file=${archive##*/}
    [ -f LICENSE ] && mv LICENSE LICENSE-${file%%-*}
    [ -f README ]  && mv README  README-${file%%-*}

    tar xzf $archive 'package*xml'
    [ -f package2.xml ] && mv package2.xml ${file%%-*}.xml \
                        || mv package.xml  ${file%%-*}.xml
done
cp %{SOURCE1} .

%build
# This is an empty build section.

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=%{_sysconfdir}
export PHP_PEAR_SIG_KEYDIR=%{_sysconfdir}/pearkeys
export PHP_PEAR_SIG_BIN=%{_root_bindir}/gpg
export PHP_PEAR_INSTALL_DIR=%{peardir}

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{_localstatedir}/cache/php-pear

# We fix this in post, and update the 'temp_dir' setting
# to use _localstatedir/tmp/php-pear instead.
export PHP_PEAR_TEMP_DIR=/var/tmp

install -d $RPM_BUILD_ROOT%{peardir} \
           $RPM_BUILD_ROOT%{_localstatedir}/cache/php-pear \
           $RPM_BUILD_ROOT%{_localstatedir}/tmp/php-pear \
           $RPM_BUILD_ROOT%{_localstatedir}/www/html \
           $RPM_BUILD_ROOT%{metadir}/pkgxml \
           $RPM_BUILD_ROOT%{_docdir}/pecl \
           $RPM_BUILD_ROOT%{_datadir}/tests/pecl \
           $RPM_BUILD_ROOT%{_sysconfdir}/pear \
           $RPM_BUILD_ROOT%{_sysconfdir}/php.d

export INSTALL_ROOT=$RPM_BUILD_ROOT
pwd
%{_bindir}/php --version

%{_bindir}/php -dmemory_limit=64M -dshort_open_tag=0 -dsafe_mode=0 \
         -d 'error_reporting=E_ALL&~E_DEPRECATED' -ddetect_unicode=0 \
         install-pear.php --force \
                 --dir      %{peardir} \
                 --cache    %{_localstatedir}/cache/php-pear \
                 --download %{_localstatedir}/tmp/php-pear/cache \
                 --config   %{_sysconfdir}/pear \
                 --bin      %{_bindir} \
                 --www      %{_localstatedir}/www/html \
                 --doc      %{_docdir}/pear \
                 --test     %{_datadir}/tests/pear \
                 --data     %{_datadir}/pear-data \
                 --metadata %{metadir} \
                 %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}

install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pear
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{_bindir}/pecl
install -m 755 %{SOURCE12} $RPM_BUILD_ROOT%{_bindir}/peardev

# Need to touch pecl.ini so it can write to it
touch $RPM_BUILD_ROOT%{_sysconfdir}/php.d/02-pecl.ini

# Fix path in SCL
for exe in pear pecl peardev; do
    sed -e 's:/usr:%{_prefix}:' \
        -i $RPM_BUILD_ROOT%{_bindir}/$exe
done

# Sanitize the pear.conf
%{_bindir}/php %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf ext_dir >new-pear.conf
%{_bindir}/php %{SOURCE3} new-pear.conf http_proxy > $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf

%{_bindir}/php -r "print_r(unserialize(substr(file_get_contents('$RPM_BUILD_ROOT%{_sysconfdir}/pear.conf'),17)));"

# Why this file here ?
rm -rf $RPM_BUILD_ROOT/.depdb* $RPM_BUILD_ROOT/.lock $RPM_BUILD_ROOT/.channels $RPM_BUILD_ROOT/.filemap

# Need for re-registrying XML_Util
install -m 644 *.xml $RPM_BUILD_ROOT%{metadir}/pkgxml

%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep '"/tmp"' $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep /usr/local $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep -rl $RPM_BUILD_ROOT $RPM_BUILD_ROOT && exit 1

%clean
rm -rf $RPM_BUILD_ROOT
rm new-pear.conf

%pre
# Manage relocation of metadata, before update to pear
if [ -d %{peardir}/.registry -a ! -d %{metadir}/.registry ]; then
  mkdir -p %{metadir}
  mv -f %{peardir}/.??* %{metadir}
fi

%post
# force new value as pear.conf is (noreplace)
current=$(%{_bindir}/pear config-get temp_dir system)
if [ "$current" == "/var/tmp" ]; then
%{_bindir}/pear config-set \
    temp_dir %{_localstatedir}/tmp/php-pear \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get test_dir system)
if [ "$current" != "%{_datadir}/tests/pear" ]; then
%{_bindir}/pear config-set \
    test_dir %{_datadir}/tests/pear \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get data_dir system)
if [ "$current" != "%{_datadir}/pear-data" ]; then
%{_bindir}/pear config-set \
    data_dir %{_datadir}/pear-data \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get metadata_dir system)
if [ "$current" != "%{metadir}" ]; then
%{_bindir}/pear config-set \
    metadata_dir %{metadir} \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get -c pecl doc_dir system)
if [ "$current" != "%{_docdir}/pecl" ]; then
%{_bindir}/pear config-set \
    -c pecl \
    doc_dir %{_docdir}/pecl \
    system >/dev/null || :
fi

current=$(%{_bindir}/pear config-get -c pecl test_dir system)
if [ "$current" != "%{_datadir}/tests/pecl" ]; then
%{_bindir}/pear config-set \
    -c pecl \
    test_dir %{_datadir}/tests/pecl \
    system >/dev/null || :
fi

%{_bindir}/pear config-set \
    php_ini %{_scl_root}/etc/php.d/02-pecl.ini \
    system >/dev/null || :

# Remove with EA3
# Stopgap measure to ensure that the cPanel interface for PEAR works
# on new servers that never had EA3 installed.
if [ ! -e "/usr/local/bin/pear" ]; then
    ln -s %{_bindir}/pear /usr/local/bin/pear;
fi

%postun
if [ $1 -eq 0 -a -d %{metadir}/.registry ] ; then
  rm -rf %{metadir}/.registry
fi

# Remove with EA3
if [ $1 -eq 0 -a -h "/usr/local/bin/pear" -a "$(readlink /usr/local/bin/pear)" = "%{_bindir}/pear" ]; then
    echo "Removing pear symlink: /usr/local/bin/pear";
    rm /usr/local/bin/pear;
fi

%files
%defattr(-,root,root,-)
%{peardir}
%dir %{metadir}
%{metadir}/.channels
%verify(not mtime size md5) %{metadir}/.depdb
%verify(not mtime)          %{metadir}/.depdblock
%verify(not mtime size md5) %{metadir}/.filemap
%verify(not mtime)          %{metadir}/.lock
%if 0%{?nfsmountable}
%dir %{_scl_root}/var
%dir %{_scl_root}/var/lib
%endif
%{metadir}/.registry
%{metadir}/pkgxml
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/pear.conf
%dir %{_localstatedir}/cache/php-pear
%dir %{_localstatedir}/tmp/php-pear
%dir %{_sysconfdir}/pear
%attr(0664,root,root) %config(noreplace) %{_sysconfdir}/php.d/02-pecl.ini
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc README*
%dir %{_docdir}/pear
%doc %{_docdir}/pear/*
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl
%{_datadir}/tests/pear
%{_datadir}/pear-data

%changelog
* Thu Nov 02 2017  Dan Muey <dan@cpanel.net> - 1.10.1-10
- EA-6910: Move pecl's php.ini to php.d/02-pecl.ini so it loads after 01-ioncube.ini

* Thu Aug 30 2017 Dan Muey <dan@cpanel.net> - 1.10.1-9
- ZC-2834: Stop using local.ini

* Thu Aug 24 2017 Dan Muey <dan@cpanel.net> - 1.10.1-8
- ZC-2819: Add support for php 7.2

* Thu Mar 23 2017 Jeffrey Royer <jeffrey.royer@cpanel.net> - 1.10.1-7
- PIG-2903: Enable PECL extensions by default

* Fri Dec 16 2016 Jacob Perkins <jacob.perkins@cpanel.net> - 1.10.1-6
- EA-5493: Added vendor field

* Tue Aug 02 2016 Edwin Buck <e.buck@cpanel.net> - 1.10.1-5
- EA-4954: Add support for php71 (beta)

* Mon Jun 20 2016 Dan Muey <dan@cpanel.net> - 1.10.1-4
- EA-4383: Update Release value to OBS-proof versioning

* Wed Jun 15 2016 Rishwanth Yeddula <rish@cpanel.net> 1.10.1-cp3
- Set 'download_dir' to a SCL path instead of using /tmp

* Tue May 31 2016 Rishwanth Yeddula <rish@cpanel.net> 1.10.1-cp2
- Create a symlink to the 'pear' script at /usr/local/bin/pear

* Mon May 16 2016 Rishwanth Yeddula <rish@cpanel.net> 1.10.1-cp1
- Initial implementation of PEAR/PECL for EA4 SCL-PHP package

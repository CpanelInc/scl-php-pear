OBS_PROJECT := EA4
scl-php81-pear-obs : DISABLE_BUILD += repository=CentOS_6.5_standard
scl-php80-pear-obs : DISABLE_BUILD += repository=CentOS_6.5_standard
scl-php72-pear-obs : DISABLE_BUILD += repository=xUbuntu_20.04
scl-php71-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=xUbuntu_20.04
scl-php70-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=xUbuntu_20.04
scl-php56-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=xUbuntu_20.04
scl-php55-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=xUbuntu_20.04
scl-php54-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=xUbuntu_20.04
OBS_PACKAGE := scl-php-pear
include $(EATOOLS_BUILD_DIR)obs-scl.mk

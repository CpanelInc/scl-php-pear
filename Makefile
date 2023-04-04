OBS_PROJECT := EA4
scl-php82-pear-obs : DISABLE_BUILD += repository=CentOS_6.5_standard
scl-php81-pear-obs : DISABLE_BUILD += repository=CentOS_6.5_standard
scl-php80-pear-obs : DISABLE_BUILD += repository=CentOS_6.5_standard
scl-php74-pear-obs : DISABLE_BUILD += repository=CentOS_9 repository=xUbuntu_22.04
scl-php73-pear-obs : DISABLE_BUILD += repository=CentOS_9 repository=xUbuntu_22.04
scl-php72-pear-obs : DISABLE_BUILD += repository=xUbuntu_20.04 repository=CentOS_9 repository=xUbuntu_22.04
scl-php71-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04 repository=xUbuntu_22.04
scl-php70-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04 repository=xUbuntu_22.04
scl-php56-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04 repository=xUbuntu_22.04
scl-php55-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04 repository=xUbuntu_22.04
scl-php54-pear-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04 repository=xUbuntu_22.04
OBS_PACKAGE := scl-php-pear
include $(EATOOLS_BUILD_DIR)obs-scl.mk

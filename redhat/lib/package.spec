%global _python_bytecompile_extra 0
#
# this is for centos7:
#
%global _python_bytecompile_errors_terminate_build 0
%global debug_package %{nil}

%global __arch_install_post [ "%{buildarch}" = "noarch" ] || QA_CHECK_RPATHS=1 ; case "${QA_CHECK_RPATHS:-}" in [1yY]*) /usr/lib/rpm/check-rpaths ;; esac ; %{_topdir}/check-buildroot

Name:           %name
Version:        %version
Release:        %{!release:1}%{?dist}
Summary:        The PATRIC Command Line Interface

License:        MIT
URL:            https://patricbrc.org/
Source0:        %source

BuildRequires:  perl-File-Slurp gcc-c++ expat-devel rsync
Requires:       perl expat

AutoReqProv: no

%description

The PATRIC Command Line Interface.

%prep
%autosetup


%build

#
# P3 release code creates binaries with embedded path
# settings so force modifications here.
#
export PERL5LIB_ADDITIONS=/vagrant/perl/lib/perl5
export PATH_ADDITIONS=/vagrant/perl/bin

env KB_IGNORE_MISSING_DEPENDENCIES=1 ./bootstrap /usr
source ./user-env.sh
#
# user-env whacks PERL5LIB so eval here to get local environment
#
eval `perl -Mlocal::lib=/vagrant/perl`

make

%install
export QA_RPATHS=$(( 0x0001|0x0010 ))

mkdir -p %{buildroot}/usr/share/%name-%version/local

source ./user-env.sh

eval `perl -Mlocal::lib=%{buildroot}/usr/share/%name-%version/local`

# PERL MODULES

perl auto-deploy \
     --target %{buildroot}/usr/share/%name-%version \
     --override KB_OVERRIDE_TOP=/usr/share/%name-%version \
     --override KB_OVERRIDE_PERL_PATH=/usr/share/%name-%version/lib:/usr/share/%name-%version/local/lib/perl5 \
     --override KB_OVERRIDE_PYTHON_PATH=/usr/share/%name-%version/lib \
     deploy.cfg

echo "/usr/share/%name-%version" > %{_topdir}/files
mkdir -p %{buildroot}/usr/bin

for file in %{buildroot}/usr/share/%name-%version/bin/*; do
    b=`basename $file`
    ln -s /usr/share/%name-%version/bin/$b %{buildroot}/usr/bin/$b
    echo "/usr/bin/$b" >> %{_topdir}/files
done

%files -f %{_topdir}/files

%changelog
* Wed Apr 17 2019 vagrant
- 

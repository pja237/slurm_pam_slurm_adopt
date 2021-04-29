# vim: sw=4:ts=4:et

%define selinux_policyver 0.0.0

Name:   slurm_pam_slurm_adopt_selinux
Version:	20.11
Release:	5%{?dist}
Summary:	SELinux policy module for slurm_pam_slurm_adopt

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	slurm_pam_slurm_adopt.pp
Source1:	slurm_pam_slurm_adopt.if



Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for slurm_pam_slurm_adopt.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/

install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/slurm_pam_slurm_adopt.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r slurm_pam_slurm_adopt
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/slurm_pam_slurm_adopt.pp
%{_datadir}/selinux/devel/include/contrib/slurm_pam_slurm_adopt.if



%changelog
* Wed Jul  3 2019 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version


# slurm_pam_slurm_adopt selinux policy package (module)

The goal is to make `pam_slurm_adopt.so` work on selinux enabled nodes in enforcing mode.

Quote from reference: [pam_slurm_adopt](https://slurm.schedmd.com/pam_slurm_adopt.html)

```
Limitations

Alternate authentication methods such as multi-factor authentication may break process adoption with pam_slurm_adopt.

SELinux may conflict with pam_slurm_adopt, so it might need to be disabled.
```

This package:

1. Creates slurm_spool_t label and applies it on /var/spool/slurm/ (rec.)
2. Creates type enforcement rules that allow sshd_t to do certain ops on the slurm_spool_t (hand-picked ones, as _narrow_ as possible)

## Updating, Building and Installing

Sometimes new features are added to slurm, e.g. centralised config in 20.x (if i remember correctly) which will change the access pattern and require type enforcement rules to be changed.

1. Edit .te files to update the TE rules appropriately (optionaly .fc if needed)
2. Bump the policy module version in .te file to match slurms (purely cosmetics, doesn't have to be modified at all)
3. Bump the rpm package version in .spec file (Version and Release) (also we match slurm version, but not necessary at all)
4. Run `slurm_pam_slurm_adopt.sh` to build rpm package
5. rpm can be found under noarch/
6. Deploy

```
root@test:~/src/slurm_pam_slurm_adopt/code#grep policy_module slurm_pam_slurm_adopt.te
policy_module(slurm_pam_slurm_adopt, 20.11.5)

root@test:~/src/slurm_pam_slurm_adopt/code#grep -E 'Release|Version' *.spec
Version:        20.11
Release:        5%{?dist}

root@test:~/src/slurm_pam_slurm_adopt/code#./slurm_pam_slurm_adopt.sh 
Building and Loading Policy
+ make -f /usr/share/selinux/devel/Makefile slurm_pam_slurm_adopt.pp

...

Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.Dh4rS0
+ umask 022
+ cd /root/src/slurm_pam_slurm_adopt/code
+ /usr/bin/rm -rf /root/src/slurm_pam_slurm_adopt/code/.build/slurm_pam_slurm_adopt_selinux-20.11-5.el8.x86_64
+ exit 0

root@test:~/src/slurm_pam_slurm_adopt/code#find noarch/
noarch/
noarch/slurm_pam_slurm_adopt_selinux-1.0-1.el8.noarch.rpm
noarch/slurm_pam_slurm_adopt_selinux-1.2-1.el8.noarch.rpm
noarch/slurm_pam_slurm_adopt_selinux-1.3-1.el8.noarch.rpm
noarch/slurm_pam_slurm_adopt_selinux-1.4-1.el8.noarch.rpm
noarch/slurm_pam_slurm_adopt_selinux-1.5-1.el8.noarch.rpm
noarch/slurm_pam_slurm_adopt_selinux-20.11-5.el8.noarch.rpm

```


## NOTES:

### install development package

```
root@test:~/src/selinux/slurm_pam_slurm_adopt#yum provides sepolicy
Updating Subscription Management repositories.
Last metadata expiration check: 1:42:02 ago on Tue 02 Jul 2019 02:53:31 PM CEST.
policycoreutils-devel-2.8-16.1.el8.i686 : SELinux policy core policy devel utilities
Repo        : rhel-8-for-x86_64-baseos-rpms
Matched from:
Filename    : /usr/bin/sepolicy

policycoreutils-devel-2.8-16.1.el8.x86_64 : SELinux policy core policy devel utilities
Repo        : rhel-8-for-x86_64-baseos-rpms
Matched from:
Filename    : /usr/bin/sepolicy

root@test:~/src/selinux/slurm_pam_slurm_adopt#yum install policycoreutils-devel -y

...

Installed:
  policycoreutils-devel-2.8-16.1.el8.x86_64                                                                                                        selinux-policy-devel-3.14.1-61.el8.noarch

Complete!
```

**man sepolicy-generate**

### initialize 

`sepolicy generate --customize -d sshd_t -n slurm_pam_slurm_adopt`

* edit fc, if, et files

* build policy

## SOURCES:
* <https://debian-handbook.info/browse/stable/sect.selinux.html>
* <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html-single/selinux_users_and_administrators_guide/index>
* <http://www.cse.psu.edu/~trj1/cse543-f07/slides/03-PolicyConcepts.pdf>
* <http://freecomputerbooks.com/books/The_SELinux_Notebook-4th_Edition.pdf>

## Reference policy
* <https://github.com/TresysTechnology/refpolicy>

## On disk help:

* /usr/share/selinux/devel/include/support/

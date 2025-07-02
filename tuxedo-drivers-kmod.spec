%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     tuxedo-drivers-kmod
Version:  4.14.2
Release:  1%{?dist}
Summary:  Tuxedo drivers as kmod
License:  GPL-2.0-or-later
URL:      https://gitlab.com/tuxedocomputers/development/packages/tuxedo-drivers

Source:   %{url}/-/archive/v%{version}/tuxedo-drivers-v%{version}.tar.gz

BuildRequires: kmodtool
BuildRequires: kernel-devel
BuildRequires: make
BuildRequires: gcc

Provides: tuxedo-drivers = %{version}
Obsoletes: tuxedo-drivers < 4.0.0

%description
Tuxedo drivers as kmod

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
%setup -q -n tuxedo-drivers-v%{version}

for kernel_version  in %{?kernel_versions} ; do
  cp -a src _kmod_build_${kernel_version%%___*}
done

%build
echo "Build stage -----------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  make V=1 %{?_smp_mflags} -C /lib/modules/${kernel_version%%___*}/build M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
echo "Install stage ---------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}/lib/modules/${kernel_version%%___*}/extra/tuxedo-drivers/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/**/*.ko %{buildroot}/lib/modules/${kernel_version%%___*}/extra/tuxedo-drivers/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}/lib/modules/${kernel_version%%___*}/extra/tuxedo-drivers/
  chmod a+x %{buildroot}/lib/modules/${kernel_version%%___*}/extra/tuxedo-drivers/*.ko
done

# Copy configs
mkdir -p %{buildroot}/%{_sysconfdir}/modprobe.d/
cp tuxedo_keyboard.conf %{buildroot}/%{_sysconfdir}/modprobe.d/tuxedo_keyboard.conf

# Copy udev rules
mkdir -p %{buildroot}/usr/lib/udev/rules.d/
cp 99-z-tuxedo-systemd-fix.rules %{buildroot}/usr/lib/udev/rules.d/
cp 99-infinityflex-touchpanel-toggle.rules %{buildroot}/usr/lib/udev/rules.d/

# Copy udev hwdb
mkdir -p %{buildroot}/usr/lib/udev/hwdb.d/
cp 61-sensor-infinityflex.hwdb %{buildroot}/usr/lib/udev/hwdb.d/

%{?akmod_install}

%files
/usr/lib/udev/rules.d/99-z-tuxedo-systemd-fix.rules
/usr/lib/udev/rules.d/99-infinityflex-touchpanel-toggle.rules
/usr/lib/udev/hwdb.d/61-sensor-infinityflex.hwdb
%doc README.md
%license debian/copyright

%config(noreplace) %{_sysconfdir}/modprobe.d/tuxedo_keyboard.conf

%changelog

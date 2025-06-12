%if 0%{?fedora}
%global debug_package %{nil}
%endif

%global short tuxedo-drivers
%global module_names tuxedo_compatibility_check tuxedo_keyboard clevo_acpi clevo_wmi uniwill_wmi tuxedo_io tuxedo_nb02_nvidia_power_ctrl ite_8291 ite_8291_lb ite_8297 ite_829x tuxedo_nb05_ec tuxedo_nb05_power_profiles tuxedo_nb05_sensors tuxedo_nb05_keyboard tuxedo_nb05_kbd_backlight tuxedo_nb05_fan_control tuxedo_nb04_keyboard tuxedo_nb04_wmi_ab tuxedo_nb04_wmi_bs tuxedo_nb04_sensors tuxedo_nb04_power_profiles tuxedo_nb04_kbd_backlight stk8321 gxtp7380 tuxedo_tuxi_fan_control tuxi_acpi

Name:     %{short}-kmod-common
Version:  4.14.0
Release:  1%{?dist}
Summary:  Tuxedo drivers kmod common files
License:  GPL-2.0-or-later
URL:      https://github.com/gladion136/tuxedo-drivers-kmod

Requires: %{short}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Tuxedo drivers kmod common files

%prep

%build

for module in %{module_names}; do
  echo "$module" > ${module}.conf
  install -D -m 0644 ${module}.conf %{buildroot}%{_modulesloaddir}/${module}.conf
done

%install
mkdir -p %{buildroot}%{_modulesloaddir}
for module in %{module_names}; do
    echo "$module" > ${module}.conf
    install -D -m 0644 ${module}.conf %{buildroot}%{_modulesloaddir}/${module}.conf
done

%files
%{_modulesloaddir}/*.conf

%changelog

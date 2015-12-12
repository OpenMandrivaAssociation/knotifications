%define major 5
%define libname %mklibname KF5Notifications %{major}
%define devname %mklibname KF5Notifications -d
%define debug_package %{nil}
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name: knotifications
Version:	5.17.0
Release:	1
Source0: http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
Summary: The KDE Frameworks 5 system notifications library
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF5Service)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5WindowSystem)
BuildRequires: cmake(KF5IconThemes)
BuildRequires: cmake(Phonon4Qt5)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Test)
Requires: %{libname} = %{EVRD}

%description
KNotifications is an abstraction to system notifications.

%package -n %{libname}
Summary: The KDE Frameworks 5 system notifications library
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
KNotifications is an abstraction to system notifications.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/KDE and Qt
Requires: %{libname} = %{EVRD}

%description -n %{devname}
KNotifications is an abstraction to system notifications.

%prep
%setup -q
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build

L="`pwd`/%{name}.lang"
cd %{buildroot}
for i in .%{_datadir}/locale/*/LC_MESSAGES/*.qm; do
	LNG=`echo $i |cut -d/ -f5`
	echo -n "%lang($LNG) " >>$L
	echo $i |cut -b2- >>$L
done

%files -f %{name}.lang
%{_datadir}/dbus-1/interfaces/*
%{_datadir}/kservicetypes5/knotificationplugin.desktop

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KF5Notifications
%{_libdir}/qt5/mkspecs/modules/*

%define major 5
%define libname %mklibname KF5Notifications %{major}
%define devname %mklibname KF5Notifications -d
%define debug_package %{nil}
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name: knotifications
Version: 5.5.0
Release: 1
Source0: http://ftp5.gwdg.de/pub/linux/kde/%{stable}/frameworks/%{version}/%{name}-%{version}.tar.xz
Summary: The KDE Frameworks 5 system notifications library
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: cmake(KF5Service)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5WindowSystem)
BuildRequires: cmake(KF5IconThemes)
BuildRequires: cmake(Phonon4Qt5)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: qmake5
BuildRequires: extra-cmake-modules5
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
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON

%build
ninja -C build

%install
DESTDIR="%{buildroot}" ninja install -C build

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

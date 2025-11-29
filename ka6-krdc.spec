#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		krdc
Summary:	krdc
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	c93742c3fe905f3300e3750ccd92b9a1
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	freerdp3-devel >= 3.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kbookmarks-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kdnssd-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-knotifyconfig-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	libssh-devel
BuildRequires:	libvncserver-devel >= 0.9
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-kbookmarks >= %{kframever}
Requires:	kf6-kcmutils >= %{kframever}
Requires:	kf6-kcompletion >= %{kframever}
Requires:	kf6-kconfig >= %{kframever}
Requires:	kf6-kconfigwidgets >= %{kframever}
Requires:	kf6-kcoreaddons >= %{kframever}
Requires:	kf6-kdnssd >= %{kframever}
Requires:	kf6-ki18n >= %{kframever}
Requires:	kf6-knotifications >= %{kframever}
Requires:	kf6-knotifyconfig >= %{kframever}
Requires:	kf6-kservice >= %{kframever}
Requires:	kf6-kwallet >= %{kframever}
Requires:	kf6-kwidgetsaddons >= %{kframever}
Requires:	kf6-kwindowsystem >= %{kframever}
Requires:	kf6-kxmlgui >= %{kframever}
Requires:	libvncserver >= 0.9
Suggests:	freerdp2-x11
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KRDC is a client application that allows you to view or even control
the desktop session on another machine that is running a compatible
server. VNC and RDP is supported.

%description -l pl.UTF-8
KRDC jest aplikacją kliencką, która pozwala oglądać a nawet
kontrolować sesję desktopową na zdalnej maszynie, na której jest
uruchomiony kompatybilny serwer. Wspierane są VNC i RDP.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DFREERDP_EXECUTABLE:PATH=/usr/bin/xfreerdp \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/krdc
%{_libdir}/libkrdccore.so.*.*
%ghost %{_libdir}/libkrdccore.so.5
%dir %{_libdir}/qt6/plugins/krdc
%dir %{_libdir}/qt6/plugins/krdc/kcms
%{_libdir}/qt6/plugins/krdc/kcms/libkcm_krdc_rdpplugin.so
%{_libdir}/qt6/plugins/krdc/kcms/libkcm_krdc_vncplugin.so
%{_libdir}/qt6/plugins/krdc/krdc_rdpplugin.so
%{_libdir}/qt6/plugins/krdc/krdc_testplugin.so
%{_libdir}/qt6/plugins/krdc/krdc_vncplugin.so
%{_desktopdir}/org.kde.krdc.desktop
%{_datadir}/config.kcfg/krdc.kcfg
%{_datadir}/metainfo/org.kde.krdc.appdata.xml
%{_datadir}/qlogging-categories6/krdc.categories
%{_datadir}/mime/packages/org.kde.krdc-mime.xml
%{_iconsdir}/hicolor/scalable/apps/krdc.svg

%files devel
%defattr(644,root,root,755)
%{_includedir}/krdc
%{_includedir}/krdccore_export.h
%{_libdir}/libkrdccore.so

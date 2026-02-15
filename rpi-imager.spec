%define tzdata_version 2025c

Name:			rpi-imager
Version:		2.0.6
Release:		1
Summary:		Graphical user-interface to write disk images and format SD cards
Group:			File tools
License:		Apache-2.0
URL:			https://github.com/raspberrypi/rpi-imager
Source0:		https://github.com/raspberrypi/rpi-imager/archive/v%{version}/%{name}-%{version}.tar.gz
##################################
# NOTE Patch0 Removes vendoring as upstream failed to provide an option for-
# NOTE downstream maintainers: see https://github.com/raspberrypi/rpi-imager/issues/924
# NOTE A subsequent attempt to get upstream to support system package usage instead of
# NOTE vendoring on 21-08-2025 also failed - https://github.com/raspberrypi/rpi-imager/pull/1175
##################################
# NOTE Upstream rapsberrypi foundation developers are heavily pushing AppImage
# NOTE over distrubution provided software.
# NOTE This is antithetical to core Linux and OSS principles of user choice.
# NOTE As described by one of their developers in git issues it as a brand-protective
# NOTE choice they made over users maintaining their software freedoms.
##################################
# NOTE Patch0 will need checked and refactored on each upstream release to ensure-
# NOTE we can use our system libs and avoid using upstream forced vendored packages.
Patch0:		rpi-imager-2.0.6-remove-vendoring.patch
##################################
# Upstream are shipping with cmake files for timezone generation which point
# to non-existant files as fallbacks for when generation fails - which it does
# in CI isolated builds, fix those so rpi-imager can set timezones for the
# the images it creates.
# Patch submitted upstream: https://github.com/raspberrypi/rpi-imager/pull/1514
Patch1: rpi-imager-2.0.6-fix-broken-timezones.patch
# Fix a missing import in WritingStep.qml causing a Qt exception for Non-attached object.
# Patch submitted upstream: https://github.com/raspberrypi/rpi-imager/pull/1515
Patch2: rpi-imager-2.0.6-fix-missing-import.patch

# QML: fix property name mismatch in ImFileDialog https://github.com/raspberrypi/rpi-imager/pull/1505
Patch20:	https://github.com/raspberrypi/rpi-imager/pull/1505/commits/25a477e9ef8d25ff17dfb3f331c7559eaf812f53.patch

BuildRequires:  appstream-util
BuildRequires:	atomic-devel
BuildRequires:	cmake
BuildRequires:	cmake(zstd)
BuildRequires:  desktop-file-utils
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libcurl-gnutls)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libnghttp2)
BuildRequires:	pkgconfig(liburing)
BuildRequires:	pkgconfig(nettle)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(Qt63DQuickRender)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Concurrent)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6LabsSynchronizer)
BuildRequires:	pkgconfig(Qt6Linguist)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6QmlAssetDownloader)
BuildRequires:	pkgconfig(Qt6QmlNetwork)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:	pkgconfig(Qt6QuickControls2Material)
BuildRequires:	pkgconfig(Qt6QuickControls2MaterialStyleImpl)
BuildRequires:	pkgconfig(Qt6QuickLayouts)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(udisks2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qt6-qtdeclarative
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:	qt6-qtbase-tools
BuildRequires:	qt6-qttools
BuildRequires:	util-linux

Requires:		hicolor-icon-theme
Requires:		dosfstools
Requires:		util-linux
# Required if you want to be able to run rpi-imager as a regular user
Requires:		udisks

%description
Graphical user-interface to download and write Raspberry Pi disk images, or
write custom disk images and format SD cards.

%prep
%autosetup -p1

%build
# Disabling the cmake options for timezone|regdb|capital_cities generation
# also disables the use of the fallback files from the tarball, thus we have to
# keep enabled options that attempt to download reasources it can never reach,
# they will fail and use the files from the source tarball instead.
pushd src
%cmake \
	-DIMAGER_VERSION_STR=%{version} \
	-DENABLE_CHECK_VERSION=OFF \
	-DENABLE_TELEMETRY=OFF \
	-G Ninja
%ninja_build
popd

%install
# install rpi-imager
pushd src
	%ninja_install -C build
popd

# install man directory in buildroot
install -dpm 0755 %{buildroot}%{_mandir}/man1
# move man pages from builddir to buildroot mandir
mv doc/man/* %{buildroot}%{_mandir}/man1

# install polkit actions
install -Dpm644 debian/com.raspberrypi.rpi-imager.policy %{buildroot}%{_datadir}/polkit-1/actions/com.raspberrypi.rpi-imager.policy

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.raspberrypi.rpi-imager.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.raspberrypi.%{name}.metainfo.xml

##################################
%files
%{_bindir}/%{name}
%{_datadir}/applications/com.raspberrypi.rpi-imager.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/polkit-1/actions/com.raspberrypi.rpi-imager.policy
%{_mandir}/man1/*.1*
%{_metainfodir}/com.raspberrypi.%{name}.metainfo.xml
%license license.txt
%doc README.md

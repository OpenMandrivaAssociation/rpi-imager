Name:			rpi-imager
Version:		1.9.6
Release:		1
Summary:		Graphical user-interface to write disk images and format SD cards
Group:			File tools
License:		Apache-2.0
URL:			https://github.com/raspberrypi/rpi-imager
Source0:		https://github.com/raspberrypi/rpi-imager/archive/v%{version}/%{name}-%{version}.tar.gz
##################################
# NOTE Patch0 Removes vendoring as upstream failed to provide an option to-
# NOTE downstream maintainers: see https://github.com/raspberrypi/rpi-imager/issues/924
# NOTE a subsequent attempt to get upstream to support system package usage instead of
# NOTE vendoring on 21-0802925 also failed - https://github.com/raspberrypi/rpi-imager/pull/1175
##################################
# NOTE Upstream rapsberrypi foundation developers are heavily pushing AppImage over distrubution provided software
# NOTE This is antithetical to core Linux and OSS principles of user choice.
# NOTE As described by one of their developers in git issues it as a brand-protective
# NOTE choice they made over having software freedoms.
##################################
# NOTE Patch0 will need checked and refactored on each upstream release to ensure-
# NOTE we can use our system libs and avoid using upstream forced vendored packages.
Patch0:			rpi-imager-1.9.6-remove-vendoring.patch
##################################

BuildRequires:	atomic-devel
BuildRequires:	cmake
BuildRequires:	cmake(zstd)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(liblzma)
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
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(udisks2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:	util-linux

Requires:		hicolor-icon-theme
Requires:		dosfstools
Requires:		util-linux
Requires:		udisks

# Needed if you want to be able to run rpi-imager as a regular user

%description
Graphical user-interface to download and write Raspberry Pi disk images, or
write custom disk images and format SD cards.

##################################
%prep
%autosetup -p1

mkdir -p ./src/build/doc/man/
cp ./doc/man/* ./src/build/doc/man/


##################################
%build
pushd src
	#-DBUILD_SHARED_LIBS=ON \
export LDFLAGS="%{optflags} -lcurl"
%cmake -GNinja \
	-DENABLE_VENDORING=OFF \
	-DENABLE_CHECK_VERSION=OFF \
	-DENABLE_TELEMETRY=OFF
%ninja_build
popd

##################################
%install
# install man directory in buildroot
install -dpm 0755 %{buildroot}%{_mandir}/man1
# compress manpage & remove input file after compression
zstd -r --rm ./src/build/doc/man/
# move man pages from builddir to buildroot mandir
mv ./src/build/doc/man/* %{buildroot}%{_mandir}/man1

# install rpi-imager
pushd src
%ninja_install -C build
popd

##################################
%files
%{_bindir}/%{name}
%{_datadir}/applications/org.raspberrypi.rpi-imager.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/*.1*
%{_metainfodir}/org.raspberrypi.%{name}.metainfo.xml
%license license.txt
%doc README.md

Name:			rpi-imager
Version:		1.9.0
Release:		3
Summary:		Graphical user-interface to write disk images and format SD cards
Group:			File tools
License:		Apache-2.0
URL:			https://github.com/raspberrypi/rpi-imager
Source0:		https://github.com/raspberrypi/rpi-imager/archive/v%{version}/%{name}-%{version}.tar.gz
##################################
# NOTE Patch0 Removes vendoring as upstream failed to provide an option to-
# NOTE downstream maintainers: see https://github.com/raspberrypi/rpi-imager/issues/924
##################################
# NOTE Patch0 will need checked and refactored on each upstream release to ensure-
# NOTE we can use our system libs and avoid using upstream vendored packages.
Patch0:			rpi-imager-1.9.0-remove-vendoring.patch
##################################

BuildRequires:	cmake
BuildRequires:	cmake(zstd)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	util-linux

Requires:		hicolor-icon-theme
Requires:		dosfstools
Requires:		util-linux

# Needed if you want to be able to run rpi-imager as a regular user
Recommends:		udisks

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

##################################
%files
%{_bindir}/%{name}
%{_datadir}/applications/org.raspberrypi.rpi-imager.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/*.1*
%{_metainfodir}/%{name}.metainfo.xml
%license license.txt
%doc README.md

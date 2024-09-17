Name:           rpi-imager
Version:        1.9.0
Release:        1
Summary:        Graphical user-interface to write disk images and format SD cards
Group:		      File tools 
License:        Apache-2.0
URL:            https://github.com/raspberrypi/rpi-imager
Source0:        https://github.com/raspberrypi/rpi-imager/archive/v%{version}/%{name}-%{version}.tar.gz
 
BuildRequires:  make
BuildRequires:  cmake
#BuildRequires:  cmake(Qt5LinguistTools)
#BuildRequires:  qt5-qtbase-devel
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  util-linux
 
Requires:       hicolor-icon-theme
Recommends:     udisks2
 
Requires:       dosfstools
 
%description
Graphical user-interface to download and write Raspberry Pi disk images, or
write custom disk images and format SD cards.
 
%prep
%autosetup -p1

%build
pushd src
export LDFLAGS="%{optflags} -lcurl"
%cmake
%make_build

%install
pushd src
%make_install -C build

%files
%{_bindir}/%{name}
%{_datadir}/applications/org.raspberrypi.rpi-imager.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_metainfodir}/%{name}.metainfo.xml
%license license.txt
%doc README.md

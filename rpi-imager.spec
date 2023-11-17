Name:           rpi-imager
Version:        1.8.3
Release:        1
Summary:        Graphical user-interface to write disk images and format SD cards
Group:		      File tools 
License:        Apache-2.0
URL:            https://github.com/raspberrypi/rpi-imager
Source0:        https://github.com/raspberrypi/rpi-imager/archive/v%{version}/%{name}-%{version}.tar.gz
 
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  qt5-qtbase-devel
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(Qt5QuickControls2)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(gnutls)
 
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
desktop-file-install \
    --add-category="X-GNOME-Utilities" \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
 
 
%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_metainfodir}/%{name}.metainfo.xml
%license license.txt
%doc README.md

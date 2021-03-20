%global debug_package %{nil}
%global __strip /bin/true

Name:           ndi-sdk
Version:        4.6.1
Release:        1%{?dist}
Summary:        NewTek NDI SDK

License:        Proprietary
URL:            https://ndi.tv/sdk
Source0:        https://downloads.ndi.tv/SDK/NDI_SDK_Linux/InstallNDISDK_v4_Linux.tar.gz
Source1:        ndi.pc.in

ExclusiveArch: i686 x86_64 armv7hl

Requires:       %{name}%{?_isa} = %{version}-%{release}


%description
NewTek NDI SDK.

%package -n libndi-sdk
Summary:        Libraries files for %{name}


%description -n libndi-sdk
The libndi-sdk package contains libraries for %{name}.


%package devel
Summary:        Libraries/include files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package documentation
Summary:        Documentation for %{name}

%description documentation
The %{name}-documentation documentations for %{name}.



%prep
%autosetup -c

# Uncompress installer
ARCHIVE=$(awk '/^__NDI_ARCHIVE_BEGIN__/ { print NR+1; exit 0; }' InstallNDISDK_v4_Linux.sh)
tail -n+$ARCHIVE InstallNDISDK_v4_Linux.sh | tar -xz
mv 'NDI SDK for Linux'/* .


%build
# Nothing to build


%install
_arch=$(uname -m)

case ${_arch} in
  armv7l)
    _ndi_arch="arm-rpi3-linux-gnueabihf"
    ;;
  i386)
    _ndi_arch=i686-linux-gnu
    ;;
  i686|x86_64)
    _ndi_arch=${_arch}-linux-gnu
    ;;
  *)
    echo "Architecture not included"
    exit 2
    ;;
esac

# Install lib/bin as appropriate
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
install -pm 0755 bin/${_ndi_arch}/ndi* %{buildroot}%{_bindir}
install -pm 0755 lib/${_ndi_arch}/libndi.so* %{buildroot}%{_libdir}
ldconfig -n %{buildroot}%{_libdir}

# Install headers
mkdir -p %{buildroot}%{_includedir}/%{name}
install -pm 0644 include/*.h %{buildroot}%{_includedir}/%{name}

# Install pc file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm 0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/ndi.pc
sed -i -e 's|@LIBDIR@|%{_libdir}|' \
  -e 's|@PREFIX@|%{_prefix}|' \
  -e 's|@VERSION@|%{version}|' \
  %{buildroot}%{_libdir}/pkgconfig/ndi.pc



%files
%{_bindir}/ndi-*

%files -n libndi-sdk
%license "NDI SDK License Agreement.pdf"  "NDI SDK License Agreement.txt" Version.txt licenses/libndi_licenses.txt
%{_libdir}/libndi.so.4*

%files devel
%doc examples
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/ndi.pc

%files documentation
%doc documentation


%changelog
* Wed Feb 24 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.6.1-1
- Initial spec file
Summary:	TomsFastMath - large integer arithmetic library
Summary(pl.UTF-8):	TomsFastMath - duża biblioteka arytmetyki na dużych liczbach całkowitych
Name:		tomsfastmath
Version:	0.13.1
Release:	1
License:	Public Domain or WTFPL v2
Group:		Libraries
#Source0Download: https://github.com/libtom/tomsfastmath/releases
Source0:	https://github.com/libtom/tomsfastmath/releases/download/v%{version}/tfm-%{version}.tar.xz
# Source0-md5:	123569cd5362e228ae5670543a4d006d
URL:		http://www.libtom.net/TomsFastMath/
BuildRequires:	libtool >= 2:1.5
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TomsFastMath is a fast public domain, open source, large integer
arithmetic library written in portable ISO C. It is a port of
LibTomMath with optional support for inline assembler multipliers.

%description -l pl.UTF-8
TomsFastMath to szybka, mająca otwarte źródła (na zasadzie public
domain) biblioteka arytmetyki na dużych liczbach całkowitych, napisana
w przenośnym ISO C. Jest to port LibTomMath z opcjonalną obsługą
procedur mnożenia w asemblerze.

%package devel
Summary:	Header files for TomsFastMath library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki TomsFastMath
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for TomsFastMath library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki TomsFastMath.

%package static
Summary:	Static TomsFastMath library
Summary(pl.UTF-8):	Statyczna biblioteka TomsFastMath
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static TomsFastMath library.

%description static -l pl.UTF-8
Statyczna biblioteka TomsFastMath.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags} -fomit-frame-pointer" \
%{__make} -f makefile.shared \
	CC="%{__cc}" \
	IGNORE_SPEED=1 \
	LIBPATH=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -f makefile.shared install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBPATH=%{_libdir} \
	INSTALL_GROUP="$(id -g)" \
	INSTALL_USER="$(id -u)"

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md SPONSORS changes.txt
%attr(755,root,root) %{_libdir}/libtfm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtfm.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/tfm.pdf
%attr(755,root,root) %{_libdir}/libtfm.so
%{_libdir}/libtfm.la
%{_includedir}/tfm.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtfm.a

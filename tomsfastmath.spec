# TODO: reenable x86 asm if newer gcc succeeds to build it
Summary:	TomsFastMath - large integer arithmetic library
Summary(pl.UTF-8):	TomsFastMath - duża biblioteka arytmetyki na dużych liczbach całkowitych
Name:		tomsfastmath
Version:	0.12
Release:	1
License:	Public Domain
Group:		Libraries
Source0:	http://libtom.org/files/tfm-%{version}.tar.bz2
# Source0-md5:	821edbffb03502f0614c8717bda6fd54
URL:		http://libtom.org/?page=features&whatfile=tfm
BuildRequires:	libtool >= 2:1.5
BuildRequires:	sed >= 4.0
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

%{__sed} -i -e 's/\<gcc\>/$(GCC)/' makefile.shared

%build
%ifarch %{ix86}
# gcc 4.7 fails to allocate 3 GREGs + 2 clobbered when compiling PIC
WORKAROUND="-DTFM_NO_ASM"
%else
WORKAROUND=
%endif
CFLAGS="%{rpmcflags} -fomit-frame-pointer $WORKAROUND" \
%{__make} -f makefile.shared \
	GCC="%{__cc}" \
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
%doc LICENSE SPONSORS changes.txt
%attr(755,root,root) %{_libdir}/libtfm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtfm.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/tfm.pdf
%attr(755,root,root) %{_libdir}/libtfm.so
%{_libdir}/libtfm.la
%{_includedir}/tfm.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtfm.a

%define major 4
%define libname %mklibname pq++ %{major}
%define devname %mklibname pq++ -d

Summary:	C++ interface for PostgreSQL
Name:		libpq++
Version:	4.0
Release:	18
License:	BSD
Group:		System/Libraries
Url:		http://gborg.postgresql.org/project/libpqpp/projdisplay.php
Source0:	%{name}-%{version}.tar.bz2
Patch0:		libpq++-4.0-Makefile.patch
Patch1:		libpq++-4.0-gcc43.patch
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(openssl)

%description
This is the C++ interface that has shipped as part of PostgreSQL
until v7.2.3.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	C++ interface for PostgreSQL
Group:		System/Libraries

%description -n %{libname}
This is the C++ interface that has shipped as part of PostgreSQL
until v7.2.3.

%files -n %{libname}
%doc CHANGES README
%{_libdir}/lib*.so.*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development library and header files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	pq++-devel = %{EVRD}
Provides:	libpq++-devel = %{EVRD}

%description -n %{devname}
This is the C++ interface that has shipped as part of PostgreSQL
until v7.2.3.

This package contains the %{name} library and its header files
needed to compile applications such as PowerDNS, etc.

%files -n %{devname}
%doc docs/*
%{_includedir}/pgsql/*.h
%{_includedir}/pgsql/libpq++/*.h
%{_libdir}/lib*.so
%{_libdir}/lib*.a

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p0

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

%build
%serverbuild

%make CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} %{ldflags} -fPIC"

%install
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/pgsql/libpq++

install -m644 libpq++.h %{buildroot}%{_includedir}/pgsql/
install -m644 pgconnection.h %{buildroot}%{_includedir}/pgsql/libpq++/
install -m644 pgdatabase.h %{buildroot}%{_includedir}/pgsql/libpq++/
install -m644 pgtransdb.h %{buildroot}%{_includedir}/pgsql/libpq++/
install -m644 pgcursordb.h %{buildroot}%{_includedir}/pgsql/libpq++/
install -m644 pglobject.h %{buildroot}%{_includedir}/pgsql/libpq++/

install -m755 libpq++.so.%{major}.0 %{buildroot}%{_libdir}/
install -m755 libpq++.a %{buildroot}%{_libdir}/
ln -s libpq++.so.%{major}.0 %{buildroot}%{_libdir}/libpq++.so.%{major}
ln -s libpq++.so.%{major}.0 %{buildroot}%{_libdir}/libpq++.so


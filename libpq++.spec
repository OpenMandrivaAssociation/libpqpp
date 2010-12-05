%define	major 4
%define libname %mklibname pq++ %{major}
%define develname %mklibname pq++ -d

Summary:	C++ interface for PostgreSQL
Name:		libpq++
Version:	4.0
Release:	%mkrel 16
URL:		http://gborg.postgresql.org/project/libpqpp/projdisplay.php
License:	BSD
Source0:	%{name}-%{version}.tar.bz2
Patch0:		libpq++-4.0-Makefile.patch
Patch1:		libpq++-4.0-gcc43.patch
Group:		System/Libraries
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-libs-devel
BuildRequires:	libgcc
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is the C++ interface that has shipped as part of PostgreSQL
until v7.2.3.

%package -n	%{libname}
Summary:	C++ interface for PostgreSQL
Group:          System/Libraries

%description -n	%{libname}
This is the C++ interface that has shipped as part of PostgreSQL
until v7.2.3.

%package -n	%{develname}
Summary:	Development library and header files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	pq++-devel = %{version}-%{release}
Provides:	libpq++-devel = %{version}-%{release}
Obsoletes:	%{mklibname pq++ 4 -d}

%description -n	%{develname}
This is the C++ interface that has shipped as part of PostgreSQL
until v7.2.3.

This package contains the %{name} library and its header files
needed to compile applications such as PowerDNS, etc.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p0

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

%build

%serverbuild

%make CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} %ldflags -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc CHANGES README
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc docs/*
%{_includedir}/pgsql/*.h
%{_includedir}/pgsql/libpq++/*.h
%{_libdir}/lib*.so
%{_libdir}/lib*.a

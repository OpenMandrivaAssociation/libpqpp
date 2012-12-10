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


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 4.0-16mdv2011.0
+ Revision: 609773
- rebuild

* Mon Apr 19 2010 Funda Wang <fwang@mandriva.org> 4.0-15mdv2010.1
+ Revision: 536664
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 4.0-12mdv2008.0
+ Revision: 83721
- rebuild

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 4.0-11mdv2008.0
+ Revision: 83654
- new devel naming


* Fri Jan 19 2007 Oden Eriksson <oeriksson@mandriva.com> 4.0-10mdv2007.0
+ Revision: 110669
- rebuilt against new postgresql libs

* Fri Dec 08 2006 Oden Eriksson <oeriksson@mandriva.com> 4.0-9mdv2007.1
+ Revision: 93714
- Import libpq++

* Fri Dec 08 2006 Oden Eriksson <oeriksson@mandriva.com> 4.0-9mdv2007.1
- use the %%mkrel macro

* Thu Dec 01 2005 Oden Eriksson <oeriksson@mandriva.com> 4.0-8mdk
- rebuilt against openssl-0.9.8a

* Thu Apr 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.0-7mdk
- rebuilt against new postgresql libs
- fix requires-on-release

* Mon Jun 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.0-6mdk
- rebuilt against new deps and with gcc v3.4.x
- fix deps


#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Low-level configuration system
Name:		dconf
Version:	0.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/0.4/%{name}-%{version}.tar.bz2
# Source0-md5:	61f4a82b6f6a3c6ae2205eff347874c2
URL:		http://live.gnome.org/dconf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.25.8
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.527
Requires(post,postun):	glib2 >= 1:2.25.8
Requires:	dbus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dconf is a low-level configuration system. Its main purpose is to
provide a backend to GSettings on platforms that don't already have
configuration storage systems.

%package devel
Summary:	Header files for dconf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dconf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.25.8

%description devel
Header files for dconf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dconf.

%package static
Summary:	Static dconf library
Summary(pl.UTF-8):	Statyczna biblioteka dconf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static dconf library.

%description static -l pl.UTF-8
Statyczna biblioteka dconf.

%package apidocs
Summary:	dconf API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki dconf
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for dconf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki dconf.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-html-dir=%{_gtkdocdir} \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules
exit 0

%postun
/sbin/ldconfig

umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules
exit 0

%files
%defattr(644,root,root,755)
%doc NEWS
%attr(755,root,root) %{_bindir}/dconf
%attr(755,root,root) %{_libdir}/libdconf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdconf.so.0
%attr(755,root,root) %{_libexecdir}/dconf-service
%attr(755,root,root) %{_libdir}/gio/modules/libdconfsettings.so
%{_libdir}/girepository-1.0/dconf-0.3.typelib
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/dbus-1/system-services/ca.desrt.dconf.service

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdconf.so
%{_datadir}/gir-1.0/dconf-0.3.gir
%{_includedir}/dconf
%{_pkgconfigdir}/dconf.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libdconf.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dconf
%endif

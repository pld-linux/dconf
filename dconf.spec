#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Low-level configuration system
Name:		dconf
Version:	0.7.2
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/0.7/%{name}-%{version}.tar.bz2
# Source0-md5:	1583be314e3ea0ab483d104e791ef653
URL:		http://live.gnome.org/dconf
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	vala >= 1:0.11.4
Requires(post,postun):	glib2 >= 1:2.28.0
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
Requires:	glib2-devel >= 1:2.28.0

%description devel
Header files for dconf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dconf.

%package editor
Summary:	Configuration editor for dconf
Summary(pl.UTF-8):	Edytor konfiguracji dla dconf
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description editor
dconf-editor allows you to browse and modify dconf database.

%description editor -l pl.UTF-8
dconf-editor pozwala na przeglądanie i modyfikowanie bazy dconf.

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
%attr(755,root,root) %{_libdir}/libdconf-dbus-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdconf-dbus-1.so.0
%attr(755,root,root) %{_libexecdir}/dconf-service
%attr(755,root,root) %{_libdir}/gio/modules/libdconfsettings.so
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/dbus-1/system-services/ca.desrt.dconf.service

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdconf.so
%attr(755,root,root) %{_libdir}/libdconf-dbus-1.so
%{_includedir}/dconf
%{_includedir}/dconf-dbus-1
%{_pkgconfigdir}/dconf.pc
%{_pkgconfigdir}/dconf-dbus-1.pc
# split to a separate package?
%{_datadir}/vala/vapi/dconf.*

%files editor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dconf-editor
%{_desktopdir}/dconf-editor.desktop
%{_datadir}/dconf-editor/dconf-editor.ui

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dconf
%endif

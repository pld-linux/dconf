#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Low-level configuration system
Name:		dconf
Version:	0.5.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/0.5/%{name}-%{version}.tar.bz2
# Source0-md5:	c905497d0255fe2ba58564f9655908ab
URL:		http://live.gnome.org/dconf
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.25.10
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk+2-devel
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libgee-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	vala >= 0.8.0
Requires(post,postun):	glib2 >= 1:2.25.10
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
Requires:	glib2-devel >= 1:2.25.10

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
%attr(755,root,root) %{_libdir}/libdconf.so.0.0.0
%attr(755,root,root) %{_libdir}/libdconf.so.0
%attr(755,root,root) %{_libexecdir}/dconf-service
%attr(755,root,root) %{_libdir}/gio/modules/libdconfsettings.so
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/dbus-1/system-services/ca.desrt.dconf.service
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdconf.so
%{_includedir}/dconf
%{_pkgconfigdir}/dconf.pc
# split to a separate package?
%{_datadir}/vala/vapi/dconf.*
%{_datadir}/gir-1.0/*.gir

%files editor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dconf-editor

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dconf
%endif

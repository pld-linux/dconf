#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	vala		# do not build Vala API
#
Summary:	Low-level configuration system
Summary(pl.UTF-8):	Niskopoziomowy system konfiguracji
Name:		dconf
Version:	0.20.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/0.20/%{name}-%{version}.tar.xz
# Source0-md5:	542db78e4867ac575ec0f69f79b3eebd
URL:		http://live.gnome.org/dconf
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11.2
BuildRequires:	dbus-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.39.1
BuildRequires:	gtk+3-devel >= 3.4.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	intltool >= 0.50.0
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	tar >= 1:1.22
# not needed atm., generated files are packaged
#%{?with_vala:BuildRequires:	vala >= 2:0.17.0}
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.39.1
Requires:	dbus
Requires:	glib2 >= 1:2.39.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dconf is a low-level configuration system. Its main purpose is to
provide a backend to GSettings on platforms that don't already have
configuration storage systems.

%description -l pl.UTF-8
dconf to niskopoziomowy system konfiguracji. Głównym celem jest
dostarczenie backendu dla GSettings na platformach, które jeszcze nie
mają systemów przechowywania danych konfiguracyjnych.

%package devel
Summary:	Header files for dconf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dconf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel
Requires:	glib2-devel >= 1:2.39.1

%description devel
Header files for dconf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dconf.

%package editor
Summary:	Configuration editor for dconf
Summary(pl.UTF-8):	Edytor konfiguracji dla dconf
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme

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

%package -n bash-completion-dconf
Summary:	bash-completion for dconf
Summary(pl.UTF-8):	Bashowe uzupełnianie nazw dla dconf
Group:		Applications/Shells
Requires:	bash-completion >= 2
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-dconf
bash-completion for dconf.

%description -n bash-completion-dconf -l pl.UTF-8
Bashowe uzupełnianie nazw dla dconf.

%package -n vala-dconf
Summary:	dconf API for Vala language
Summary(pl.UTF-8):	API dconf dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.18.0

%description -n vala-dconf
dconf API for Vala language.

%description -n vala-dconf -l pl.UTF-8
API dconf dla języka Vala.

%prep
%setup -q

%build
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-html-dir=%{_gtkdocdir} \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/dconf/{db,profile}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules || :

%glib_compile_schemas

%postun
/sbin/ldconfig

umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules || :

%glib_compile_schemas

%post editor
%update_icon_cache hicolor
%update_icon_cache HighContrast

%postun editor
%update_icon_cache hicolor
%update_icon_cache HighContrast

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/dconf
%attr(755,root,root) %{_libdir}/libdconf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdconf.so.1
%attr(755,root,root) %{_libdir}/libdconf-dbus-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdconf-dbus-1.so.0
%attr(755,root,root) %{_libexecdir}/dconf-service
%attr(755,root,root) %{_libdir}/gio/modules/libdconfsettings.so
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%dir %{_sysconfdir}/dconf
%dir %{_sysconfdir}/dconf/db
%dir %{_sysconfdir}/dconf/profile
%{_mandir}/man1/dconf-service.1*
%{_mandir}/man1/dconf.1*
%{_mandir}/man7/dconf.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdconf.so
%attr(755,root,root) %{_libdir}/libdconf-dbus-1.so
%{_includedir}/dconf
%{_includedir}/dconf-dbus-1
%{_pkgconfigdir}/dconf.pc
%{_pkgconfigdir}/dconf-dbus-1.pc

%files editor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dconf-editor
%{_datadir}/appdata/dconf-editor.appdata.xml
%{_desktopdir}/dconf-editor.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/HighContrast/*/*/*.png
%{_mandir}/man1/dconf-editor.1*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dconf
%endif

%files -n bash-completion-dconf
%defattr(644,root,root,755)
%{_datadir}/bash-completion/completions/dconf

%if %{with vala}
%files -n vala-dconf
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/dconf.deps
%{_datadir}/vala/vapi/dconf.vapi
%endif

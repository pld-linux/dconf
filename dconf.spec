#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	vala		# do not build Vala API
#
Summary:	Low-level configuration system
Summary(pl.UTF-8):	Niskopoziomowy system konfiguracji
Name:		dconf
Version:	0.28.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dconf/0.28/%{name}-%{version}.tar.xz
# Source0-md5:	81faa8e68e5ea71ff0ee75050fc0759c
Patch0:		%{name}-docs-build.patch
URL:		http://live.gnome.org/dconf
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.41.0
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	tar >= 1:1.22
# not needed atm., generated files are packaged
#%{?with_vala:BuildRequires:	vala >= 2:0.18.0}
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.39.1
Requires:	dbus
Requires:	glib2 >= 1:2.44.0
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
Requires:	glib2-devel >= 1:2.44.0

%description devel
Header files for dconf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dconf.

%package apidocs
Summary:	dconf API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki dconf
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-dconf
dconf API for Vala language.

%description -n vala-dconf -l pl.UTF-8
API dconf dla języka Vala.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Denable-gtk-doc=%{__true_false apidocs}

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/dconf/{db,profile}
install -d $RPM_BUILD_ROOT%{_datadir}/dconf/profile

%meson_install -C build

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

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

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/dconf
%attr(755,root,root) %{_libdir}/libdconf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdconf.so.1
%attr(755,root,root) %{_libexecdir}/dconf-service
%attr(755,root,root) %{_libdir}/gio/modules/libdconfsettings.so
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%dir %{_sysconfdir}/dconf
%dir %{_sysconfdir}/dconf/db
%dir %{_sysconfdir}/dconf/profile
%dir %{_datadir}/dconf
%dir %{_datadir}/dconf/profile
%{_mandir}/man1/dconf-service.1*
%{_mandir}/man1/dconf.1*
%{_mandir}/man7/dconf.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdconf.so
%{_includedir}/dconf
%{_pkgconfigdir}/dconf.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dconf
%endif

%files -n bash-completion-dconf
%defattr(644,root,root,755)
%{bash_compdir}/dconf

%if %{with vala}
%files -n vala-dconf
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/dconf.deps
%{_datadir}/vala/vapi/dconf.vapi
%endif

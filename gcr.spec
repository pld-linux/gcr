#
# Conditional build:
%bcond_without	apidocs		# API documentation

Summary:	GObject and GUI library for high level crypto parsing and display
Summary(pl.UTF-8):	Biblioteka GObject i GUI do wysokopoziomowej analizy i wyświetlania danych kryptograficznych
Name:		gcr
Version:	3.41.1
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gcr/3.41/%{name}-%{version}.tar.xz
# Source0-md5:	c1e98af977236255006e11e8f8cfbaca
URL:		https://gitlab.gnome.org/GNOME/gcr
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 1.34.0
BuildRequires:	gtk+3-devel >= 3.22.0
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	libgcrypt-devel >= 1.4.5
BuildRequires:	libsecret-devel >= 0.20
BuildRequires:	libtasn1-devel
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.52
BuildRequires:	ninja >= 1.5
BuildRequires:	openssh-clients
BuildRequires:	p11-kit-devel >= 0.19.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.20.0
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.44.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires(post,postun):	desktop-file-utils
Requires(post,preun,postun):	systemd-units >= 1:250.1
Requires:	%{name}-ui = %{version}-%{release}
Requires:	gnupg2 >= 2.0
Requires:	hicolor-icon-theme
Requires:	libsecret >= 0.20
Requires:	systemd-units >= 1:250.1
Conflicts:	gnome-keyring < 3.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gcr is a library for displaying certificates, and crypto UI, accessing
key stores. It also provides a viewer for crypto files on the GNOME
desktop.

gck is a library for accessing PKCS#11 modules like smart cards.

%description -l pl.UTF-8
gcr to biblioteka do wyświetlania certyfikatów oraz kryptograficznego
interfejsu użytkownika, pozwalającego na dostęp do kluczy. Zapewnia
tekże przeglądarkę plików kryptograficznych dla środowiska GNOME.

gck to biblioteka dostepu do modułów PKCS#11, takich jak karty
procesorowe.

%package libs
Summary:	gcr and gck libraries
Summary(pl.UTF-8):	Biblioteki gcr i gck
Group:		Libraries
Requires:	glib2 >= 1:2.44.0
Requires:	libgcrypt >= 1.4.5
Requires:	p11-kit >= 0.19.0
Obsoletes:	gnome-keyring-libs < 3.3.0

%description libs
This package provides gcr and gck libraries.

%description libs -l pl.UTF-8
Ten pakiet dostarcza biblioteki gcr i gck.

%package devel
Summary:	Header files for gcr and gck libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek gcr i gck
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44.0
Requires:	p11-kit-devel >= 0.19.0
Obsoletes:	gcr-static < 3.36.0
Obsoletes:	gcr-ui-static < 3.36.0
Obsoletes:	gnome-keyring-devel < 3.3.0

%description devel
Header files for gcr and gck libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek gcr i gck.

%package -n vala-gcr
Summary:	gcr and gck API for Vala language
Summary(pl.UTF-8):	API gcr i gck dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.20.0
BuildArch:	noarch

%description -n vala-gcr
gcr and gck API for Vala language.

%description -n vala-gcr -l pl.UTF-8
API gcr i gck dla języka Vala.

%package ui
Summary:	gcr UI library
Summary(pl.UTF-8):	Biblioteka interfejsu użytkownika gcr
Group:		X11/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk+3 >= 3.22.0

%description ui
gcr UI library.

%description ui -l pl.UTF-8
Biblioteka interfejsu użytkownika gcr.

%package ui-devel
Summary:	Header files for gcr-ui library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gcr-ui
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-ui = %{version}-%{release}
Requires:	gtk+3-devel >= 3.22.0

%description ui-devel
Header files for gcr-ui library.

%description ui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gcr-ui.

%package -n vala-gcr-ui
Summary:	gcr-ui API for Vala language
Summary(pl.UTF-8):	API gcr-ui dla języka Vala
Group:		X11/Development/Libraries
Requires:	%{name}-ui-devel = %{version}-%{release}
Requires:	vala-gcr = %{version}-%{release}
BuildArch:	noarch

%description -n vala-gcr-ui
gcr-ui API for Vala language.

%description -n vala-gcr-ui -l pl.UTF-8
API gcr-ui dla języka Vala.

%package apidocs
Summary:	gcr and gck API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek gcr i gck
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	gnome-keyring-apidocs < 3.3.0
BuildArch:	noarch

%description apidocs
API and gck documentation for gcr library.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek gcr i gck.

%prep
%setup -q

%build
%meson build \
	-Dgpg_path=%{__gpg} \
	-Dgtk_doc=%{__true_false apidocs}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gc* $RPM_BUILD_ROOT%{_gidocdir}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database_post
%systemd_user_post gcr-ssh-agent.service

%preun
%systemd_user_preun gcr-ssh-agent.service

%postun
%glib_compile_schemas
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database_postun
%systemd_user_postun_with_restart gcr-ssh-agent.service

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	ui -p /sbin/ldconfig
%postun	ui -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CONTRIBUTING.md NEWS README.md
%attr(755,root,root) %{_bindir}/gcr-viewer
%attr(755,root,root) %{_libexecdir}/gcr-prompter
%attr(755,root,root) %{_libexecdir}/gcr-ssh-agent
%attr(755,root,root) %{_libexecdir}/gcr-ssh-askpass
%{systemduserunitdir}/gcr-ssh-agent.service
%{systemduserunitdir}/gcr-ssh-agent.socket
%{_desktopdir}/gcr-prompter.desktop
%{_desktopdir}/gcr-viewer.desktop
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp.convert
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp_keyservers.convert
%{_datadir}/dbus-1/services/org.gnome.keyring.PrivatePrompter.service
%{_datadir}/dbus-1/services/org.gnome.keyring.SystemPrompter.service
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp.gschema.xml
%{_datadir}/mime/packages/gcr-crypto-types.xml
%{_iconsdir}/hicolor/*x*/apps/gcr-*.png

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgck-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgck-1.so.0
%attr(755,root,root) %{_libdir}/libgcr-base-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcr-base-3.so.1
%{_libdir}/girepository-1.0/Gck-1.typelib
%{_libdir}/girepository-1.0/Gcr-3.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgck-1.so
%attr(755,root,root) %{_libdir}/libgcr-base-3.so
%{_datadir}/gir-1.0/Gck-1.gir
%{_datadir}/gir-1.0/Gcr-3.gir
%{_includedir}/gck-1
%dir %{_includedir}/gcr-3
%dir %{_includedir}/gcr-3/gcr
%{_includedir}/gcr-3/gcr/gcr-*.h
%{_pkgconfigdir}/gck-1.pc
%{_pkgconfigdir}/gcr-base-3.pc

%files -n vala-gcr
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gck-1.deps
%{_datadir}/vala/vapi/gck-1.vapi
%{_datadir}/vala/vapi/gcr-3.deps
%{_datadir}/vala/vapi/gcr-3.vapi
%{_datadir}/vala/vapi/pkcs11.vapi

%files ui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgcr-ui-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcr-ui-3.so.1
%{_libdir}/girepository-1.0/GcrUi-3.typelib

%files ui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgcr-ui-3.so
%{_datadir}/gir-1.0/GcrUi-3.gir
%{_includedir}/gcr-3/gcr/gcr.h
%{_includedir}/gcr-3/ui
%{_pkgconfigdir}/gcr-3.pc
%{_pkgconfigdir}/gcr-ui-3.pc

%files -n vala-gcr-ui
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gcr-ui-3.deps
%{_datadir}/vala/vapi/gcr-ui-3.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/gck-1
%{_gidocdir}/gcr-3
%{_gidocdir}/gcr-ui-3
%endif

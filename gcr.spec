#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	GObject and GUI library for high level crypto parsing and display
Summary(pl.UTF-8):	Biblioteka GObject i GUI do wysokopoziomowej analizy i wyświetlania danych kryptograficznych
Name:		gcr
Version:	3.4.0
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gcr/3.4/%{name}-%{version}.tar.xz
# Source0-md5:	16c49fa1a6d5bbb1f37b94880c1bbedb
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	gnupg
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libtasn1-devel
BuildRequires:	libtool
BuildRequires:	p11-kit-devel >= 0.6
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun):	glib2 >= 1:2.30.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires(post,postun):	desktop-file-utils
Requires:	gnupg
Requires:	hicolor-icon-theme
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
Requires:	glib2 >= 1:2.30.0
Requires:	libgcrypt >= 1.2.2
Requires:	p11-kit >= 0.6
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
Requires:	glib2-devel >= 1:2.30.0
Requires:	p11-kit-devel >= 0.6
Obsoletes:	gnome-keyring-devel < 3.3.0

%description devel
Header files for gcr and gck libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek gcr i gck.

%package static
Summary:	Static gcr and gck libraries
Summary(pl.UTF-8):	Statyczne biblioteki gcr i gck
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	gnome-keyring-static < 3.3.0

%description static
Static gcr and gck libraries.

%description static -l pl.UTF-8
Statyczne biblioteki gcr i gck.

%package apidocs
Summary:	gcr and gck API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek gcr i gck
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	gnome-keyring-apidocs < 3.3.0

%description apidocs
API and gck documentation for gcr library.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek gcr i gck.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I build/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--disable-update-mime \
	--disable-update-icon-cache \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmock-test-module.*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database_post

%postun
%glib_compile_schemas
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database_postun

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README
%attr(755,root,root) %{_bindir}/gcr-viewer
%attr(755,root,root) %{_libexecdir}/gcr-prompter
%{_desktopdir}/gcr-prompter.desktop
%{_desktopdir}/gcr-viewer.desktop
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp.convert
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp_keyservers.convert
%{_datadir}/dbus-1/services/org.gnome.keyring.PrivatePrompter.service
%{_datadir}/dbus-1/services/org.gnome.keyring.SystemPrompter.service
%{_datadir}/gcr-3
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp.gschema.xml
%{_datadir}/mime/packages/gcr-crypto-types.xml
%{_iconsdir}/hicolor/*/*/*.png

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgck-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgck-1.so.0
%attr(755,root,root) %{_libdir}/libgcr-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcr-3.so.1
%attr(755,root,root) %{_libdir}/libgcr-base-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcr-base-3.so.1
%{_libdir}/girepository-1.0/Gck-1.typelib
%{_libdir}/girepository-1.0/Gcr-3.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgck-1.so
%attr(755,root,root) %{_libdir}/libgcr-3.so
%attr(755,root,root) %{_libdir}/libgcr-base-3.so
%{_datadir}/gir-1.0/Gck-1.gir
%{_datadir}/gir-1.0/Gcr-3.gir
%{_includedir}/gck-1
%{_includedir}/gcr-3
%{_pkgconfigdir}/gck-1.pc
%{_pkgconfigdir}/gcr-3.pc
%{_pkgconfigdir}/gcr-base-3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgck-1.a
%{_libdir}/libgcr-3.a
%{_libdir}/libgcr-base-3.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gck
%{_gtkdocdir}/gcr-3
%endif

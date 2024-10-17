%define bigfov 0
# --with plf build libpano with fov > 160 support wich is patent covered
# or have some legal issue, so disabled by default

%{?_with_plf: %{expand: %%global bigfov 1}}

%define name	libpano12
%define version 2.8.6
%define	rel	6
%if %bigfov
%define distsuffix plf
%endif

%define	release	%mkrel %{rel}

%define lib_major 0
%define libname %mklibname pano12_ %{lib_major}
%define develname %mklibname -d pano12

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Panorama Tools library
License:	GPL
Group:		System/Libraries
Source:		%{name}-%{version}.tar.gz
URL:		https://panotools.sourceforge.net/
BuildRequires:	java-1.7.0-icedtea-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Utilies for Helmut Dersch's Panorama Tools.

%if %bigfov
This package is in PLF because there is a patent if FOV is > 160
%endif

%package -n %{libname}
Summary:	Panorama Tools library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	libpano0
Provides:	libpano0

%description -n %{libname}
Libraries for Helmut Dersch's Panorama Tools.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	pano12-devel = %{version}-%{release}
Obsoletes:  %mklibname -d %{name}_ 0

%description -n %{develname}
Developent headers for Helmut Dersch's Panorama Tools.

%prep
%setup -q

%build
export LIBS="-lm"
%if %bigfov
perl -pi -e "s|\#define\s+MAX_FISHEYE_FOV.*|\#define MAX_FISHEYE_FOV 3600|" filter.h
%endif
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure2_5x --enable-shared=yes --enable-static=no --disable-rpath
%make

%install
rm -rf %{buildroot}
%makeinstall
chmod 644 %{buildroot}/%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files 
%defattr (-,root,root)
%doc gpl.txt README.linux README.windows
%{_bindir}/PT*
%{_bindir}/pano12info

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/libpano12.so.*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/pano12
%{_libdir}/libpano12.la
%{_libdir}/libpano12.so


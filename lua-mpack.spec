#%{!?lua_version: %global lua_version %(lua -e "print(string.sub(_VERSION, 5))")}
%global lua_version 5.3
%global lua_libdir %{_libdir}/lua/%{lua_version}
%global lua_pkgdir %{_datadir}/lua/%{lua_version}

%global libmpack_version 1.0.5

BuildRequires:  libtool
BuildRequires:  lua >= 5.3
BuildRequires:  lua-devel >= 5.3

Name:           lua-mpack
Version:        1.0.6
Release:        2%{?dist}

License:        MIT
Summary:        Implementation of MessagePack for Lua
Url:            https://github.com/libmpack/libmpack-lua

Requires:       lua(abi) = %{lua_version}

Source0:        https://github.com/libmpack/libmpack-lua/archive/%{version}/libmpack-lua-%{version}.tar.gz
Source1:        https://github.com/libmpack/libmpack/archive/%{version}/libmpack-%{libmpack_version}.tar.gz

Patch0:         lmpack_lua_5_3.patch
Patch1:         lmpack_makefile.patch

%description
mpack is a small binary serialization/RPC library that implements
both the msgpack and msgpack-rpc specifications.

%prep
%setup -q -n libmpack-lua-%{version}

%patch0 -p1
%patch1 -p1

mkdir mpack-src
pushd mpack-src
tar xfz %{SOURCE1} --strip-components=1
popd

# hack to export flags
echo '#!/bin/sh' > ./configure
chmod +x ./configure

%build

%configure
make %{?_smp_mflags} \
     USE_SYSTEM_LUA=yes \
     MPACK_LUA_VERSION=%{lua_version} \
     LUA_LIB="$(pkg-config --libs lua)" \

%install
make USE_SYSTEM_LUA=yes \
     LUA_CMOD_INSTALLDIR=%{lua_libdir} \
     DESTDIR=%{buildroot} \
     install

%files
%defattr(-,root,root)
%doc README.md
%{lua_libdir}/mpack.so

%changelog
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 08 2017 Andreas Schneider <asn@redhat.com> - 1.0.6-1
- Update to 1.0.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Andreas Schneider <asn@redhat.com> - 1.0.4-1
- resolves: #1417325 - Update to version 1.0.4

* Fri Nov 25 2016 Andreas Schneider <asn@redhat.com> - 1.0.3-5
- Add requirement on ABI version and do not package lua directory

* Thu Nov 24 2016 Andreas Schneider <asn@redhat.com> - 1.0.3-4
- Add the license correctly in the files section

* Tue Nov 15 2016 Andreas Schneider <asn@redhat.com> - 1.0.3-3
- Create a configure script so we export all flags

* Tue Nov 15 2016 Andreas Schneider <asn@redhat.com> - 1.0.3-2
- Removed Group:
- Removed BuildRoot:

* Mon Nov 14 2016 Andreas Schneider <asn@redhat.com> - 1.0.3-1
- Initial version 1.0.3

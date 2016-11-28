%{!?lua_version: %global lua_version %(lua -e "print(string.sub(_VERSION, 5))")}
%global lua_libdir %{_libdir}/lua/%{lua_version}
%global lua_pkgdir %{_datadir}/lua/%{lua_version}

BuildRequires:  libtool
BuildRequires:  lua >= 5.3
BuildRequires:  lua-devel >= 5.3

Name:           lua-mpack
Version:        1.0.3
Release:        5%{?dist}

License:        MIT
Summary:        Implementation of MessagePack for Lua
Url:            https://github.com/tarruda/libmpack/

Requires:       lua(abi) = %{lua_version}

Source0:        https://github.com/tarruda/libmpack/archive/%{version}/libmpack-%{version}.tar.gz
Patch0:         libmpack-1.0.3-fix_macro_redefine.patch

%description
mpack is a small binary serialization/RPC library that implements
both the msgpack and msgpack-rpc specifications.

%prep
%setup -q -n libmpack-%{version}

%patch0 -p1 -b .libmpack-1.0.3-fix_macro_redefine.patch

# hack to export flags
pushd binding/lua
echo '#!/bin/sh' > ./configure
chmod +x ./configure
popd

%build
pushd binding/lua
%configure
make %{?_smp_mflags} \
     USE_SYSTEM_LUA=yes \
     LUA_VERSION_MAJ_MIN=%{lua_version} \
     LUA_LIB=$(pkg-config --libs lua)
popd

%install
pushd binding/lua
make USE_SYSTEM_LUA=yes \
     LUA_CMOD_INSTALLDIR=%{lua_libdir} \
     DESTDIR=%{buildroot} \
     install
popd

%files
%defattr(-,root,root)
%license LICENSE-MIT
%doc README.md
%{lua_libdir}/mpack.so

%changelog
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

%global gitcommit a735bfbfb2e23a3817086c24d4d80ac539058967
%{?gitcommit:%global gitcommitshort %(c=%{gitcommit}; echo ${c:0:7})}

Name:           dynamomd
Version:        1.7.4364
Release:        2%{?commit:.git%{commitshort}}%{?dist}
Summary:        Event-driven particle simulation sofware

License:        unknown
URL:            http://dynamomd.org/
Source0:        https://github.com/toastedcrumpets/DynamO/archive/%{?gitcommit}.tar.gz#/%{name}-%{gitcommitshort}.tar.gz

Patch0001:      0001-cmake-add-usr-lib64-to-search-list-of-cairommconfig..patch

%global num_patches %{lua: c=0; for i,p in ipairs(patches) do c=c+1; end; print(c);}

BuildRequires:  python
BuildRequires:  boost-devel
BuildRequires:  boost-static
BuildRequires:  bzip2-devel
BuildRequires:  Judy-devel
#BuildRequires:  cairomm-devel
#BuildRequires:  ffmpeg-devel
#BuildRequires:  freeglut-devel
#BuildRequires:  glew-devel
#BuildRequires:  gtkmm30-devel
#BuildRequires:  libpng-devel
#BuildRequires:  libXmu-devel

BuildRequires:  cmake
BuildRequires:  git

Provides:  %{name} = %{version}-%{release}

%description
%{summary}.

%prep
%setup -q -n DynamO-%{gitcommit}
%if %{num_patches}
git init
git config user.email "watanabe.yu@gmail.com"
git config user.name "Yu Watanabe"
git add .
git commit -a -q -m "%{version} baseline."
# Apply all the patches.
git am %{patches}
%endif

%build
mkdir build
pushd build
%cmake ..
popd
%make_build -C build

%install
%make_install -C build
# copyright is installed by %%license command
rm -f %{buildroot}%{_datadir}/doc/dynamomd/copyright

%check
# skip tests as they take so long time...
#make test -C build

%files
%license copyright
%{_bindir}/*

%changelog
* Thu Feb 08 2018 Yu Watanabe <watanabe.yu@gmail.com> - 1.7.4364-2.gita735bfb
- do not build visualiser

* Thu Feb 08 2018 Yu Watanabe <watanabe.yu@gmail.com> - 1.7.4364-1.gita735bfb
- Initial release

%global gitcommit 8d6f9d43f9b8fe714d5699971cc114f5d2bf5df8
%{?gitcommit:%global gitcommitshort %(c=%{gitcommit}; echo ${c:0:7})}

Name:           dynamomd
Version:        1.7.4
Release:        1%{?commit:.git%{commitshort}}%{?dist}
Summary:        Event-driven particle simulation sofware

License:        GPLv3
URL:            http://dynamomd.org/
Source0:        https://github.com/toastedcrumpets/DynamO/archive/%{gitcommit}/%{name}-%{gitcommitshort}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  python
BuildRequires:  boost-devel
BuildRequires:  boost-static
BuildRequires:  bzip2-devel
BuildRequires:  Judy-devel

# required for dynamo visualizer
#BuildRequires:  cairomm-devel
#BuildRequires:  ffmpeg-devel
#BuildRequires:  freeglut-devel
#BuildRequires:  glew-devel
#BuildRequires:  gtkmm30-devel
#BuildRequires:  libpng-devel
#BuildRequires:  libXmu-devel

Provides:  %{name} = %{version}-%{release}

%description
%{summary}.

%prep
%setup -q -n DynamO-%{gitcommit}

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
* Mon Nov 26 2018 Yu Watanabe <watanabe.yu@gmail.com> - 1.7.4-1.git8d6f9d4
- Update to latest git snapshot 8d6f9d43f9b8fe714d5699971cc114f5d2bf5df8

* Sat Feb 10 2018 Yu Watanabe <watanabe.yu@gmail.com> - 1.7-3.git03563cd
- Update to upstream snapshot 03563cde8a3504ae602ff1a2b67b7831e599ee66

* Thu Feb 08 2018 Yu Watanabe <watanabe.yu@gmail.com> - 1.7-2.gita735bfb
- do not build visualizer

* Thu Feb 08 2018 Yu Watanabe <watanabe.yu@gmail.com> - 1.7-1.gita735bfb
- Initial release

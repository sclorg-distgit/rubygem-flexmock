%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global	ruby_sitelib		%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

%global	gem_name	flexmock

Summary:	Mock object library for ruby
Name:		%{?scl_prefix}rubygem-%{gem_name}
Version:	2.0.4
Release:	3%{?dist}
Group:		Development/Languages
License:	Copyright only
URL:		http://flexmock.rubyforge.org
Source0:	http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Source1:	%{gem_name}-v%{version}-test-missing-files.tar.gz
# Source1 is created fron Source2
Source2:	flexmock-create-missing-test-files.sh

Requires:	%{?scl_prefix_ruby}ruby(release)
Requires:	%{?scl_prefix_ruby}ruby(rubygems)
BuildRequires:	%{?scl_prefix_ruby}ruby(release)
BuildRequires:	%{?scl_prefix_ruby}rubygems-devel
BuildRequires:	%{?scl_prefix_ruby}rubygem(minitest) >= 5
BuildRequires:	%{?scl_prefix_ruby}rubygem(test-unit)
Provides:	%{?scl_prefix}rubygem(%{gem_name}) = %{version}-%{release}
BuildArch:	noarch

%description
FlexMock is a simple, but flexible, mock object library for Ruby unit
testing.

%package	doc
Summary:	Documentation for %{pkg_name}
Group:		Documentation
Requires:	%{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description	doc
This package contains documentation for %{pkg_name}.

%package	-n %{?scl_prefix}ruby-%{gem_name}
Summary:	Non-Gem support package for %{gem_name}
Group:		Development/Languages
Requires:	%{?scl_prefix}%{pkg_name} = %{version}-%{release}
Provides:	%{?scl_prefix}ruby(%{gem_name}) = %{version}-%{release}

%description    -n %{?scl_prefix}ruby-%{gem_name}
This package provides non-Gem support for %{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T

%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

find . -name \*.rb | xargs sed -i -e '\@/usr/bin/env@d'
find . -name \*.gem -or -name \*.rb -or -name \*.rdoc | xargs chmod 0644

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

pushd %{buildroot}%{gem_instdir}
rm -rf \
	.autotest .gitignore .togglerc .travis.yml .yardopts \
	Gemfile \
	Rakefile \
	flexmock.blurb \
	flexmock.gemspec \
	install.rb

%check
pushd .%{gem_instdir}

tar xf %{SOURCE1}
mv flexmock/test .

%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:.:test \
	-e 'Dir.glob("test/*_test.rb").each {|f| require f}'
ruby -Ilib:.:test \
	-e 'gem "minitest" ; require "minitest/autorun" ; Dir.glob("test/minitest*/*_test.rb").each {|f| require f}'
%{?scl:EOF}
popd

%files
%defattr(-,root,root,-)
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*

%{gem_libdir}
%{gem_instdir}/rakelib/
%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%defattr(-,root,root,-)
%{gem_instdir}/todo.txt
%{gem_instdir}/doc/
%{gem_docdir}/

%changelog
* Tue Feb 23 2016 Pavel Valena <pvalena@redhat.com> - 2.0.4-3
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.4-1
- 2.0.4

* Wed Dec 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.3-1
- 2.0.3

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.2-1
- 2.0.2

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.1-1
- 2.0.1

* Thu Sep 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.0-1
- 2.0.0

* Fri Aug 14 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-5
- Fix two failing tests, and omit one test currently

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-3
- Force to use minitest ver4 for now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-1
- 1.3.3

* Wed Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.2-1
- 1.3.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-1
- 1.3.1

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.0-3
- Macro / BR / Requires cleanup 

* Wed Feb 27 2013 Josef Stribny <jstribny@redhat.com> - 1.3.0-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.0-1
- 1.3.0

* Tue Jan  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- 1.2.0

* Sun Nov  4 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Thu Oct 11 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.3-1
- 1.0.3

* Fri Sep 14 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.2-1
- 1.0.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-3
- F-17: rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-1
- 0.9.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.11-2
- Fix typo Provides on main package (bug 674413)

* Sun Oct 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.11-1
- 0.8.11

* Fri Jul 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.7-1
- 0.8.7

* Thu Jul 30 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.6-1
- Switch to gem, repackage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 08 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-3
- Fix repoid 

* Wed Nov 07 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-2
- Spec cleanups in response to review
- Fix license
- strip out shebangs

* Sun Sep 09 2007 Paul Nasrat <pauln@truemesh.com> - 0.7.1-1
- Initial vesion

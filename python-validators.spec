#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python Data Validation for Humans
Summary(pl.UTF-8):	Sprawdzanie poprawności danych dla ludzi
Name:		python-validators
# keep 0.14.x here for python2 support; 0.14.3 has been yanked
Version:	0.14.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/validators/
Source0:	https://files.pythonhosted.org/packages/source/v/validators/validators-%{version}.tar.gz
# Source0-md5:	ae3932b693452b96f037c919e1d7250f
Patch0:		validators-sphinx.patch
URL:		https://pypi.org/project/validators/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-decorator >= 3.4.0
#BuildRequires:	python-flake8 >= 2.4.0
#BuildRequires:	python-isort >= 4.2.2
BuildRequires:	python-pytest >= 2.2.3
BuildRequires:	python-six >= 1.4.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-decorator >= 3.4.0
#BuildRequires:	python3-flake8 >= 2.4.0
#BuildRequires:	python3-isort >= 4.2.2
BuildRequires:	python3-pytest >= 2.2.3
BuildRequires:	python3-six >= 1.4.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2 >= 1.8
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Simple validation library where validating a simple value does not
require defining a form or a schema.

%description -l pl.UTF-8
Prosta biblioteka do sprawdzania poprawności danych, w której
sprawdzanie prostej wartości nie wymaga definiowania jej postaci ani
schematu.

%package -n python3-validators
Summary:	Python Data Validation for Humans
Summary(pl.UTF-8):	Sprawdzanie poprawności danych dla ludzi
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-validators
Simple validation library where validating a simple value does not
require defining a form or a schema.

%description -n python3-validators -l pl.UTF-8
Prosta biblioteka do sprawdzania poprawności danych, w której
sprawdzanie prostej wartości nie wymaga definiowania jej postaci ani
schematu.

%package apidocs
Summary:	API documentation for Python validators module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona validators
Group:		Documentation

%description apidocs
API documentation for Python validators module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona validators.

%prep
%setup -q -n validators-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/validators
%{py_sitescriptdir}/validators-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-validators
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/validators
%{py3_sitescriptdir}/validators-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif

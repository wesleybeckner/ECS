
<a id='top'></a>

# *pythonic* package development tutorial

There are great resources out there for getting your projects documented and distributed. I got started using [shablona](https://github.com/uwescience/shablona/tree/master/doc) from the eScience institute at U Washington. I would still recommend that to folks. I've found, however, that it can be helpful to start bare-bones and walk through a tutorial to build your package up, to really understand how everything is working together. So in the following, if you follow the tutorial, you'll start with a basic directory structure, and proced to add on documentation, web hosting, continuous integration, coverage, and finally deploy your package on pypi. 

## Overview

By the grace of open-source-dev there are several free lunches you should know of:

2. [sphinx](#sphinx)
    1. sphinx can be a bit [finicky](https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/). The most important feature to introduce to you to today will be 
    2. [autodocs](https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/) where we generate documentation from just your 
    3. [docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) super cool!
1. [github pages](#ghpages)
    1. not only is it free, but read the docs has a magnicent protocol for turning your hard-earned digital documentation to a pdf. Possibly my favorite feature I'll mention today.
3. [travis CI](#travis)
    1. "CI" stands for continuous integration. These folks provide you with a free service -- up to 1 hour of CPU time on their servers to run all of your unit tests. 
4. [coveralls](#coveralls)
    1. how much of that passed build is covered?!
5. [pypi](#pypi)
    1. You want people using your code as fast as possible, right? 

<a id='sphinx'></a>

## Sphinx

[back to top](#top)

### Basic directory structure

Clone this repo and cd into the main directory. Checkout the package organization:

```
$ tree
.
├── ECS_demo
│   ├── __init__.py
│   ├── core.py
│   ├── data
│   │   ├── climate_sentiment_m1.h5
│   │   └── tweet_global_warming.csv
│   ├── input.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_ECS_demo.py
│   └── version.py
├── LICENSE
├── README.md
├── appveyor.yml
├── docs
│   ├── Makefile
│   ├── _static
│   ├── conf.py
│   ├── index.rst
│   └── source
│       ├── ECS_demo.core.rst
│       ├── ECS_demo.rst
│       └── ECS_demo.tests.rst
├── examples
│   ├── README.ipynb
│   └── README.txt
├── requirements.txt
└── setup.py
```

We're about to find out just how busy this directory structure can be with these added open source features. But for now, the main project lives under `ECS_demo/` with `tests/` and `data/` subdirectories.

Go ahead and inspect the contents of the core.py and test_ECS_demo.py files, in case you're interested. There's some common elements here in the package development world. `core.py` contains, well, the core code of the package. In a larger package you might have other modules living here such as `analysis.py` or `visualize.py`, depending on how you want to organize your code. For now, the `core.py` file contains four functions: `load_data, data_setup, baseline_model` and one class: `Benchmark`. You can learn more about pythonic naming conventions from the [pep8](https://www.python.org/dev/peps/pep-0008/) documentation.

### Makefile

Time to get to Sphinx! cd over to the docs directory. In this tutorial, I've setup the appropriate rst files already. I haven't had excellent luck with using sphinx-quickstart or sphinx-autogen, personally. And so I will always start with a template such as this and modify the `.rst` files as needed. Suffice to say, if you are interested in creating your documentation from scratch I found this [source](https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/) helpful.

All you need to do is type `make html` in the `docs/` directory where your `Makefile` is sitting. and Sphinx will generate static html documents of your site.

```
$ tree -L 2
.
├── Makefile
├── _build
│   ├── doctrees
│   └── html
├── _static
├── conf.py
├── index.rst
└── source
    ├── ECS_demo.core.rst
    ├── ECS_demo.rst
    └── ECS_demo.tests.rst
```

Use your preferred browser to checkout your site: `open _build/html/index.html`. If you navigate to the API you'll see how Sphinx autmoatically formats your docstrings for you, super neat!

<a id='ghpages'></a>

## Github Pages

[back to top](#top)

At this point we're ready to make our documentation live. Personally, my favorite method while I'm still developing a project is Github pages. This is because github allows us to directly host our statically generated files with Sphinx. As your code grows up, you'll want to migrate to something more robust like readthedocs.io. The downside of doing this initially is that readthedocs compiles your website as you push to github and little changes in your code structure or prerequisites can break the build. It's just easier to put this work off until you're at version 0.0.1.

### Github UI

In your browser, navigate to the settings folder for your cloned github project and scroll down until you see Github Pages. Change the Source option to master branch /docs folder and hit save.

### Local changes

Now in your local repo we're going to do a bit of a juggling act. We've been working in docs/ directory we'll want to move this sphinx stuff to its own home and make sure our statically generated files live here. So in your main directory this would like:
```
$ mkdir sphinx
$ mv docs/* sphinx/
$ mv sphinx/_build/html/* docs/
$ tree -L 1 docs/
├── docs
│   ├── _sources
│   ├── _static
│   ├── genindex.html
│   ├── index.html
│   ├── objects.inv
│   ├── py-modindex.html
│   ├── search.html
│   ├── searchindex.js
│   └── source
```
By default, github uses jekyll to build its' sites. We'll want to turn this feature off since our site is already built. In the `docs/` directory simply type `touch .nojekyll`. Now add/commit/push your changes. Your project is live under the url (yourgihtubname).io/ECS

<a id='travis'></a>

## Travis CI

[back to top](#top)

### Makefile

We're going to use travis to run our unit tests. Good coding practice dictates that we also check our code for readability. This is done using pep8. 

Before we do this with travis we'll want to test our code locally. Same as with the autodocumentation, a Makefile makes this job easier for this. You'll create a new Makefile in the main directory and add the following:
```
flake8: 
        @if command -v flake8 > /dev/null; then \ 
                echo "Running flake8"; \ 
                flake8 flake8 --ignore N802,N806,F401 `find . -name \*.py | grep -v setup.py | grep -v /docs/ | grep -v /sphinx/`; \ 
        else \ 
                echo "flake8 not found, please install it!"; \ 
                exit 1; \ 
        fi; 
        @echo "flake8 passed" 
```
Basically, we're asking flake8 to run some but not all, tests on some but not all, files. 

at the end of that file we'll also add:
```
test: 
        py.test 
```
You can now run `make flake8` and `make test` and see that your package passes your unittests, locally.

### requirements.txt

Travis CI needs to know how to build the environment to run our code. We'll do this with a requirements.txt file, also in the main directory:
```
keras
tensorflow
scikit-learn
pandas
```

### .travis.yml

If you haven't already, navigate over to travis-ci.org and create an account with them, then import the ECS project.

To get this up and running with travis we'll need to add a .travis.yml file:

```
language: python
sudo: false

deploy:
  provider: pypi
  user: wesleybeckner
  password:
    secure:
  on:
    tags: true
    repo: ECS

env:
  global:
    - PIP_DEPS="pytest coveralls pytest-cov flake8"

python:
  - '3.6'


install:
- travis_retry pip install $PIP_DEPS
- travis_retry pip install numpy cython
- travis_retry pip install -r requirements.txt
- travis_retry pip install -e .

before_script: # configure a headless display to test plot generation
- "export DISPLAY=:99.0"
- "sh -e /etc/init.d/xvfb start"
- sleep 3 # give xvfb some time to start

script:
- flake8 --ignore N802,N806,W503,F401 `find . -name \*.py | grep -v setup.py | grep -v version.py | grep -v __init__.py | grep -v /docs/ | grep -v /sphinx/`
- mkdir for_test
- cd for_test
- py.test --pyargs ECS_demo --cov-report term-missing --cov=ECS_demo
```

you'll notice that the `.travis.yml` file contains the same flake8 and py.test commands. git add/commit/push and checkout your passing travis build.

<a id='coveralls'></a>

## Coveralls 

[back to top](#top)

Other than setting up an account with coveralls and linking it to your github account, you don't have much to do here. At the end of your .travis.yml file add the following:
```

after_success:
- coveralls
```
travis ci will now pass your build to coveralls.

<a id='pypi'></a>

## pypi 

[back to top](#top)

`setup.py` contains the information that will launch our project on pypi. cd to your main directory and issue the command: `python setup.py sdist upload` (you'll need to have registered an email address + account with them before hand) 

At the end of this tutorial, your directory structure will have grown substantially!
```
$ tree -L 3
.
├── ECS_demo
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── core.cpython-36.pyc
│   │   ├── input.cpython-36.pyc
│   │   └── version.cpython-36.pyc
│   ├── core.py
│   ├── data
│   │   ├── climate_sentiment_m1.h5
│   │   └── tweet_global_warming.csv
│   ├── tests
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── test_ECS_demo.py
│   └── version.py
├── ECS_demo.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── requires.txt
│   └── top_level.txt
├── LICENSE
├── Makefile
├── README.md
├── dist
│   └── ECS_demo-0.0.dev0.tar.gz
├── docs
│   ├── _sources
│   │   ├── index.rst.txt
│   │   └── source
│   ├── _static
│   │   ├── ajax-loader.gif
│   │   ├── basic.css
│   │   ├── comment-bright.png
│   │   ├── comment-close.png
│   │   ├── comment.png
│   │   ├── css
│   │   ├── doctools.js
│   │   ├── documentation_options.js
│   │   ├── down-pressed.png
│   │   ├── down.png
│   │   ├── file.png
│   │   ├── fonts
│   │   ├── jquery-3.2.1.js
│   │   ├── jquery.js
│   │   ├── js
│   │   ├── minus.png
│   │   ├── plus.png
│   │   ├── pygments.css
│   │   ├── searchtools.js
│   │   ├── underscore-1.3.1.js
│   │   ├── underscore.js
│   │   ├── up-pressed.png
│   │   ├── up.png
│   │   └── websupport.js
│   ├── genindex.html
│   ├── index.html
│   ├── objects.inv
│   ├── py-modindex.html
│   ├── search.html
│   ├── searchindex.js
│   └── source
│       ├── ECS_demo.core.html
│       ├── ECS_demo.html
│       └── ECS_demo.tests.html
├── examples
│   ├── README.ipynb
│   ├── README.txt
│   ├── demo1.png
│   └── demo2.png
├── requirements.txt
├── setup.py
└── sphinx
    ├── Makefile
    ├── _build
    │   ├── doctrees
    │   └── html
    ├── _static
    ├── conf.py
    ├── index.rst
    └── source
        ├── ECS_demo.core.rst
        ├── ECS_demo.rst
        └── ECS_demo.tests.rst
```

## More to come

1. sdist vs bdist
2. Google cloud platform
3. Twitter API

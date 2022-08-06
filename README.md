# sboutils

Tools to manage SlackBuilds: `sboask` (shows information from [SlackBuilds.org](https://slackbuilds.org/)), `sborun` (runs a SlackBuild automatically) and `sboset` (helps with SlackBuild templates). They are written in BASH and are heavily inspired by the pkgutils and prt-get outstanding package management tools for CRUX. 

This is still a work in progress, as I am testing the tools at the moment. I will appreaciate any feedback either by email: **slackalaxy ат gmail.com**, or on irc.libera.chat: **ppetrov^**

## Requirements
* [hoorex ](https://slackbuilds.org/repository/15.0/misc/hoorex/)  (Dependency Calculator)
* configuration file should go here: `/etc/sboutils.conf`
* [template](./templates/) files should be in: `/usr/share/sboutils/templates`. These are the ones at [SBo](https://slackbuilds.org/templates/), I only added a `template.desktop` file.

## Configuration
You should adjust `/etc/sboutils.conf` accordingly. Below is my configuration:
```
# The three lines below are needed if you create new SlackBuilds by <sboset>
MAINTAINER="Petar Petrov"
EMAIL="slackalaxy at gmail dot com"
ADDRESS="$EMAIL"

# Where the SBo repo release number, SBo repo url, where the repo will be 
# synced by rsync, the whole path to the downloaded repo (this I will simplify),
# where to build and where to output packages
RELEASE="15.0"
URL="rsync://slackbuilds.org/slackbuilds/$RELEASE"
SYNC="/var/lib/sboutils"
REPO="$SYNC/$RELEASE"
BUILD="/tmp/SBo"
PKGS="/tmp"

# Specify your architecture: "x86_64" or "x86"
ARCH="x86_64"
```

## sboask
This asks SlackBuilds.org about stuff. It displays information about a SlackBuild (including immediate list of dependencies and whether they are already installed), uses [hoorex](https://slackbuilds.org/repository/15.0/misc/hoorex/) to generate a full list of dependencies, or reverse-dependencies (dependents) -- SlackBuilds that depend on the searched entry. It can also search by name or a keyword. What it **cannot** do is build and install from SBo.
```
bash-5.1$ sboask help
Usage: sboask [task] SlackBuild [-v]
Tasks:
  sync           sync with remote SlackBuilds repo
  info           display information about SlackBuild
  isinst         show if a package is installed
  dep            show dependencies chain for a SlackBuild
  dependent      show what depends on a SlackBuild
  find|search    search for a SlackBuild by name
  key            search by keyword
  help           print this help
Options:
  -v, --verbose  display a more verbose output
```
As an example, let's consider **inkscape** and display information about it, using the `info` task. This outputs the following, where dependencies *lxml*, *numpy* and *potrace* I already have installed:
```
bash-5.1$ sboask info inkscape

inkscape (Open Source vector graphics editor)
Version:  1.2
Category: graphics
Homepage: http://www.inkscape.org/

Inkscape is an Open Source vector graphics editor, with capabilities
similar to Illustrator, Freehand, CorelDraw, or Xara X using the W3C
standard Scalable Vector Graphics (SVG) file format.  Supported SVG
features include shapes, paths, text, markers, clones, alpha blending,
transforms, gradients, patterns, and grouping.  Inkscape also supports
Creative Commons meta-data, node editing, layers, complex path
operations, bitmap tracing, text-on-path, flowed text, direct XML
editing, and more.  It imports formats such as JPEG, PNG, TIFF, and
others and exports PNG as well as multiple vector-based formats.

[ ] inkscape
--- dependencies: ([i] installed, [ ] not installed)
[ ] GraphicsMagick
[ ] gdl
[ ] dos2unix
[ ] double-conversion
[ ] libcdr
[i] lxml
[i] numpy
[i] potrace
[ ] pstoedit
[ ] scour
```
Let's display the full list of **inkscape** dependencies by `dep`, which outputs a simple list, recursively:
```
bash-5.1$ sboask dep inkscape
--- dependencies: ([i] installed, [ ] not installed)
[i] numpy
[ ] dos2unix
[i] potrace
[ ] pstoedit
[ ] double-conversion
[ ] gdl
[i] python3-soupsieve
[ ] libcdr
[i] python3-webencodings
[i] python2-setuptools-scm
[ ] scour
[i] functools-lru-cache
[i] python2-soupsieve
[ ] GraphicsMagick
[i] html5lib
[i] BeautifulSoup4
[i] python2-BeautifulSoup4
[i] lxml
[ ] inkscape
```
Let's see what depends on **libgnome**, by `dependent`. I have it installed, as well as most of the SlackBuilds dependent on it:
```
bash-5.1$ sboask dependent libgnome
--- dependencies: ([i] installed, [ ] not installed)
[i] libgnome
[ ] gnome-python
[i] libbonoboui
[i] libgnomemm
```
Searching can be done either by name or a keyword. Searching for stuff with "clamav" in the name, by either `find` or `search`, will output a list, showing the category:
```
bash-5.1$ sboask find clamav
network/clamav-unofficial-sigs
system/clamav
system/squidclamav
```
As a comparison, searching by keywords with `key`, will output:
```
bash-5.1$ sboask key clamav
desktop/thunar-sendto-clamtk
network/clamav-unofficial-sigs
system/clamav
system/clamsmtp
system/clamtk
system/squidclamav
```
To quickly check if something is installed, pass `isinst`, which will return:
```
bash-5.1$ sboask isinst libgnome
[i] libgnome
```
The `--verbose` (`-v`) option can be used with each task and will tell `sboask` to output some more information, such as the short description from the slack-desc files:
```
bash-5.1$ sboask dependent libgnome -v
--- status and dependencies: ([i] installed, [ ] not installed)
[i] libgnome (Libraries needed for GNOME)
[i] libbonoboui (Independant CORBA interface support library)
[i] libgnomemm (C++ wrappers for libgnome)
[ ] gnome-python (Python bindings for GNOME)
```
When used with `info`, the sources name, md5sum and maintainer information will also be displayed, for example for **ghemical**:
```
bash-5.1$ sboask info ghemical -v

Name:     ghemical
Version:  3.0.0
Category: academic
Homepage: http://www.bioinformatics.org/ghemical/

Ghemical is an easy-to-use molecular editor with OpenGL visualisation
features and modeling package with all-atoms molecular mechanics,
reduced protein models and links to many common quantum chemistry
codes.

Keywords: ghemical, MM, QM, computational chemistry

--- sources (md5sum | filename):
becf98626f0eba73f7f042bc92aa60ac | ghemical-3.0.0.tar.gz

Maintainer: Daniil Bratashov (dn2010@gmail.com)

[ ] ghemical (Computational chemistry package)
--- status and dependencies: ([i] installed, [ ] not installed)
[i] gtkglext (an OpenGL extension to GTK)
[ ] libghemical (computational chemistry library from ghemical)
[ ] liboglappth (OpenGL extension library for GTK)
[i] openbabel (Open Babel 3D Library)
```
## sborun
This runs a SlackBuild. It should be run from within the folder containing the SlackBuild and its associated files (*.info, slack-desc,...). It can download sources, check md5sum, as well as build and install the ready package. Of course, you should have the right permissions for this.
```
Run sborun from within the SlackBuild containing folder.
Usage: sborun [options]
Options:
  -b,   --build             build package
  -i,   --install           install package
  -u,   --upgrade           upgrade package
  -ri,  --reinstall         reinstall package
  -d,   --download          download and check sources
  -nc,  --no-certificate    do not check download certificate
  -h,   --help              print this help
```
To build a package from a SlackBuild, run `sborun -b`, however, it will expect to find the sources in the folder where your SlackBuild is. To download them and then proceed with build, run it as: `sborun -d`. By default, the created package is not installed, so to do this, pass the `-i` option. This will first call `installpkg --warn`, which checks if any files already present will be overwritten and then proceeds with instalation. Therefore, if you want to automatically download source, build and install the created package, run:
```
sborun -d -b -i
```
To upgrade an older package, use `-u` in stead of `-i`. To reinstall, use the `-ri` option.
## sboset
This helps set up a new SlackBuild, by fetching the appropriate template (autotools, cmake, meson,...) and naming files accordingly. It also cleans up a bit the templates, filling the program's name automatically where needed, as well as the author's credentials. It can download sources and update md5sum, which I use for example between version updates. It should be run from within the folder where you plan your SlackBuild to be.
```
bash-5.1$ sboset -h
Run sboset from within the SlackBuild folder.
Usage: sboset [template] [option]
Templates: auto (autotools), cmake, haskell, meson,
           perl, python, ruby (rubygem)
Options:
  -di,  --doinst            copy doinst.sh file
  -du,  --douninst          copy douninst.sh file
  -de,  --desktop           copy template.desktop file
  -d,   --download          download all sources
  -c,   --clean             clean any sources
  -nc,  --no-certificate    do not check download certificate
  -um,  --update-md5        update sources md5sum
  -h,   --help              print this help
```
For example, if you want a new SlackBuild that uses **cmake**, has a **doinst.sh** and a **desktop** file, do
```
sboset cmake -di -de
```
If you are updating an old SlackBuild and want to download the new sources (already filled in the info file) and automatically update their md5sum, run it as:
```
sboset -d -um
```
For now, `sboset` can only update *preexisting* md5sum, but generating md5sum for new SlackBuilds is on my TODO list.
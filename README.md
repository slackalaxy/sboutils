# sboutils

Tools written in bash to manage SlackBuilds: `sboask` (shows information from SlackBuilds.org), `sborun` (runs a SlackBuild automatically) and `sbomake` (helps with SlackBuild templates). They are heavily inspired by the pkgutils and prt-get outstanding package management tools for CRUX. 

**I am testing sboutils at the moment, by using them to update my Slackbuilds. So, this is still very much work in progress! When I think I am done, I'll make an announcement at LQ.**

I will appreaciate any feedback: slackalaxy ат gmail.com

## Requirements
* [hoorex](https://slackbuilds.org/repository/15.0/misc/hoorex/)
* configuration file should go here: `/etc/sboutils.conf`
* [template](./templates/) files should be in: `/usr/share/sboutils/templates`. These are the ones at [SBo](https://slackbuilds.org/templates/), I only added a `template.desktop` file.

## sboask
This asks SlackBuilds.org about stuff. It displays info about a SlackBuild (including immediate list of dependencies and whether they are already installed), uses [hoorex](https://slackbuilds.org/repository/15.0/misc/hoorex/) to generate a full list of dependencies, or reverse-dependencies (dependents) -- SlackBuilds that depend on the searched entry, as well as, does some basic searching.
```
bash-5.1$ sboask help
Usage: sboask [task] SlackBuild [ -v ]
Tasks:
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
As an example, let's consider **inkscape** and display information about it, by `sboask info inkscape`. This outputs the following, where dependencies *lxml*, *numpy* and *potrace* I already have installed:
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
Let's display the full list of **inkscape** dependencies by `sboask dep inkscape`, which outputs a simple list, recursively:
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
Let's see what depends on **libgnome**, by `sboask dependent libgnome`. I have it installed, as well as most of it dependent SlackBuilds:
```
bash-5.1$ sboask dependent libgnome
--- dependencies: ([i] installed, [ ] not installed)
[i] libgnome
[ ] gnome-python
[i] libbonoboui
[i] libgnomemm
```
Searching can be done either by name or keywords. Searching for stuff with "clamav" in the name, by `sboask find clamav`, will output a list, showing the category:
```
bash-5.1$ sboask find clamav
network/clamav-unofficial-sigs
system/clamav
system/squidclamav
```
As a comparison, searching by keywords with `sboask key clamav`, will output:
```
bash-5.1$ sboask key clamav
desktop/thunar-sendto-clamtk
network/clamav-unofficial-sigs
system/clamav
system/clamsmtp
system/clamtk
system/squidclamav
```
To quickly check if something is installed, do `sboask isinst libgnome`, which will return:
```
[i] libgnome
```
The --verbose (-v) option can be used with each `task` and will tell `sboask` to output some more information, such as the short description from the slack-desc files:
```
bash-5.1$ sboask dependent libgnome -v
--- status and dependencies: ([i] installed, [ ] not installed)
[i] libgnome (Libraries needed for GNOME)
[i] libbonoboui (Independant CORBA interface support library)
[i] libgnomemm (C++ wrappers for libgnome)
[ ] gnome-python (Python bindings for GNOME)
```
When used with the `info` task, the sources name, md5sum and maintainer information will also be displayed, for example for **ghemical**:
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
This runs a SlackBuild. It should be run from within the folder containing the SlackBuild and its associated files (*.info, slack-desc,...). It can download sources, check md5sum, as well as build and install the ready package. If you just run it without any additional options it will only build the package.
```
bash-5.1$ sborun -h
Run sborun from within the SlackBuild containing folder.
Usage: sborun [options]
Options:
  -i,   --install           build and install package
  -u,   --upgrade           build and upgrade package
  -d,   --download          download, check sources and exit
  -f,   --force             force operation
  -nc,  --no-certificate    do not check download certificate
  -h,   --help              print this help
```

## sbomake
This makes a new SlackBuild, or rather it helps create it, by fetching the appropriate template (autotools, cmake, meson,...) and naming files accordingly. It also cleans up a bit, filling the program's name automatically where needed, as well as the author's credentials. It can download sources and update their md5sum, for example between version updates. It should be run from within the folder where you plan your SlackBuild to be.
```
bash-5.1$ sbomake -h
Run sbomake from within the SlackBuild folder.
Usage: sbomake [template] [option]
Templates: auto (autotools), cmake, haskell, meson,
           perl, python, ruby (rubygem)
Options:
  -di,  --doinst            copy doinst.sh file
  -du,  --douninst          copy douninst.sh file
  -de,  --desktop           copy template.desktop file
  -d,   --download          download all sources and exit
  -c,   --clean             clean any sources and exit
  -nc,  --no-certificate    do not check download certificate
  -um,  --update-md5        update sources md5sum and exit
  -h,   --help              print this help
```

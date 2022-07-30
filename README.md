# sboutils

Tools written in bash to manage SlackBuilds: `sboask` (shows information from SlackBuilds.org), `sborun` (runs a SlackBuild automatically) and `sbomake` (helps with SlackBuild templates). They are heavily inspired by the pkgtools and prt-get outstanding package management tools for CRUX.

## Requirements
* [hoorex](https://slackbuilds.org/repository/15.0/misc/hoorex/)
* configuration file should go to: `/etc/sboutils.conf`
* template files should be in: `/usr/share/sboutils/templates`

## sboask
Displays info about a SlackBuild (including immediate list of dependencies and whether they are already installed), uses [hoorex](https://slackbuilds.org/repository/15.0/misc/hoorex/) to generate a full list of dependencies or SlackBuilds that depend on the searched entry, as well as does some basic searching.
```
Usage: sboask [task] SlackBuild
Tasks:
  info           display information about SlackBuild
  dep            display dependencies chain for a SlackBuild
  dependent      display what depends on a SlackBuild
  find|search    search for a SlackBuild
  help           display this help message
```
* As an example, let's consider (inkscape), and display its info, by:
  * `sboask info inkscape`
  * this outputs, where dependencies lxml, numpy and potrace I already have installed:
```
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

--- direct dependencies: ([i] installed)
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
* Let's display the full list of inkscape dependencies:
  * `sboask dep inkscape`
  * which outputs a simple list, recursively:

```
--- dependencies: ([i] installed, [ ] not installed)
[ ] libcdr
[ ] double-conversion
[ ] dos2unix
[i] python3-webencodings
[ ] pstoedit
[i] potrace
[i] python2-setuptools-scm
[ ] scour
[ ] gdl
[i] functools-lru-cache
[i] numpy
[i] python3-soupsieve
[i] python2-soupsieve
[ ] GraphicsMagick
[i] python2-BeautifulSoup4
[i] BeautifulSoup4
[i] html5lib
[i] lxml
[ ] inkscape
```
* Let's see what depends on libgnome
  * `sboask dependent libgnome`
  * I have it installed, as well as most of it dependent SlackBuilds:
```
--- dependencies: ([i] installed, [ ] not installed)
[i] libgnome
[i] libbonoboui
[ ] gnome-python
[i] libgnomemm
```
* Finally, searching is quite simple (for now)
  * `sboask find clamav`
  * this returns a simple list, telling the category:
```
network/clamav-unofficial-sigs
system/clamav
system/squidclamav
```

## sborun
This should be run from within a folder containing a SlackBuild and it's associated files. It can download sources, check and compare md5sum, update md5sum (I use this when I make a version update), as well as build and install the ready package.
```
Run sborun from within the SlackBuild containing folder.
Usage: sborun [options]
Options:
  -i,   --install           build and install package
  -u,   --upgrade           build and upgrade package
  -w,   --warn              warn if package will overwrite files
  -r,   --rebuild           rebuild package
  -ri,  --reinstall         rebuild and reinstall package
  -d,   --download          download sources and exit
  -nc,  --no-certificate    do not check download certificate
  -cm,  --check-md5         check sources md5sum and exit
  -um,  --update-md5        update sources md5sum and exit
  -h,   --help              print this help
```

## sbomake

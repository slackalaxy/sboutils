# SBoUtils

Tools to manage SlackBuilds: `sboask` (shows information from [SlackBuilds.org](https://slackbuilds.org/)), `sborun` (runs a SlackBuild automatically) and `sboset` (helps with SlackBuild templates). They are written in BASH and are heavily inspired by the pkgutils and prt-get outstanding package management tools for CRUX. 

This is still a work in progress, as I am testing the tools at the moment. I will appreaciate any feedback either by email: **slackalaxy ат gmail.com**, or on irc.libera.chat: **ppetrov^**

## Requirements
* [hoorex ](https://slackbuilds.org/repository/15.0/misc/hoorex/)  (Dependency Calculator), used by `sboask`
* [sbo-maintainer-tools](https://slackbuilds.org/repository/15.0/system/sbo-maintainer-tools/) (sbolint and sbopkglint for SBo maintainers), `sbopkglint` used by `sborun`
* configuration file should go here: `/etc/sboutils.conf`
* [template](./templates/) files should be in: `/usr/share/sboutils/templates`. These are the ones at [SBo](https://slackbuilds.org/templates/), I only added a `template.desktop` file.

## Configuration
You should adjust `/etc/sboutils.conf` accordingly. Below is my configuration:
```
# The three lines below are needed if you create new SlackBuilds by <sboset>
MAINTAINER="Petar Petrov"
EMAIL="slackalaxy at gmail dot com"
ADDRESS="$EMAIL"

# SBo repo release number, SBo repo url, where the repo will be synced,
# the whole path to the downloaded repo (this I will simplify),
# where to build and where to output packages
RELEASE="15.0"
URL="rsync://slackbuilds.org/slackbuilds/$RELEASE"
SYNC="/var/lib/sboutils"
REPO="$SYNC/$RELEASE"
BUILDS="/tmp/SBo"
PKGS="/tmp"

# Specify your architecture: "x86_64" or "x86"
ARCH="x86_64"
```
## sboask
This asks SlackBuilds.org about stuff. It displays information about a SlackBuild (including immediate list of dependencies and whether they are already installed), uses [hoorex](https://slackbuilds.org/repository/15.0/misc/hoorex/) to generate a full list of dependencies, or reverse-dependencies (dependents) -- SlackBuilds that depend on the searched entry. It can also show all installed packages from SBo, as well as the ones with potential updates pending. Finally, `sboask` can also search by name or a keyword. What it **cannot** do is build and install from SBo.
```
bash-5.1$ sboask help
Usage: sboask [task] SlackBuild [-v]
Tasks:
  sync           sync with remote SlackBuilds repo
  info           display information about a SlackBuild
  installed      list installed packages
  updates        list potential updates of packages
  isinst         show if a package is installed
  dep            show dependencies chain for a SlackBuild
  dependent      show what depends on a SlackBuild
  find|search    search for a SlackBuild by name
  key            search by keyword
  footprint      show footprint of a package
  help           print this help
Option:
  -v, --verbose  display short description of package
```
Before start, make sure the folder where SBo repo will be downloaded exists:
```
mkdir -p /var/lib/sboutils
```
Then, `sync` with repo:
```
sboask sync
```
This will create a subfolder `15.0` -- the Slackware/SlackBuilds version that we use. Finally, point `hoorex` to the folder where the repo was downloaded. Do this also as a normal user, if you do not want to be root when using `sboask`.
```
hoorex -s /var/lib/sboutils/15.0/
```
As an example, let's consider **rstudio-desktop** and display information about it, using the `info` task. This outputs the following, with a list of immediate dependencies, indicating which ones are already installed and those with potential updates:
```
bash-5.1$ sboask info rstudio-desktop

Name:     rstudio-desktop
Version:  2022.07.1+554
Category: development
Homepage: http://rstudio.com

RStudio is a cross-platform IDE for the R statistical computing
environment. It is available in desktop and server versions.
This builds the Linux desktop version.

RStudio currently only supports 64-bit systems.

The last supported version of RStudio for 32-bit systems is 1.1.463.
A rstudio-desktop-legacy SlackBuild for 32-bit systems is available.

Keywords: R, IDE, statistics, data, analytics

[ ] rstudio-desktop
--- status: ([i] installed, [u] update, [ ] not installed)
[i] R
[u] pandoc-bin
[i] yaml-cpp
[ ] hunspell-en
[ ] yarn
[u] apache-ant
[i] zulu-openjdk8
[i] mathjax2
[ ] soci
```
Note, that if you happen to have a package installed twice, it will be marked with an error box `[e]` (not indicated in the legend, since it should not happen). Let's display the full list of **rstudio-desktop** dependencies by `dep`:
```
bash-5.1$ sboask dep rstudio-desktop
--- status: ([i] installed, [u] update, [ ] not installed)
[i] yaml-cpp
[u] apache-ant
[u] nodejs
[i] R
[u] pandoc-bin
[i] mathjax2
[ ] hunspell-en
[ ] yarn
[i] unixODBC
[i] zulu-openjdk8
[i] postgresql
[ ] soci
[ ] rstudio-desktop
```
Let's see what depends on **R**, by `dependent`, but this time we'll pass the `--verbose` option to also show the short description for each:
```
bash-5.1$ sboask dependent R --verbose
--- status: ([i] installed, [u] update, [ ] not installed)
[i] R (language and environment for statistical computing)
[ ] cistrome-mdseqpos (Cistrome Applications Harvard mdseqpos)
[ ] rstudio-desktop-legacy (R Statistical IDE)
[i] SeqMonk (A Mapped Sequence Analysis tool)
[ ] cistrome-conductGO (find the top-n highest expressed TFs)
[ ] rpy2 (R in Python)
[ ] rstudio-desktop (R Statistical IDE)
```
When used with `info`, the sources, md5sum and maintainer information will also be displayed:
```
bash-5.1$ sboask info rstudio-desktop --verbose

Name:     rstudio-desktop
Version:  2022.07.1+554
Category: development
Homepage: http://rstudio.com

RStudio is a cross-platform IDE for the R statistical computing
environment. It is available in desktop and server versions.
This builds the Linux desktop version.

RStudio currently only supports 64-bit systems.

The last supported version of RStudio for 32-bit systems is 1.1.463.
A rstudio-desktop-legacy SlackBuild for 32-bit systems is available.

Keywords: R, IDE, statistics, data, analytics

--- sources 64bit (md5sum | filename):
e57b59a213f2be140d26b122c1ea24bc | rstudio-2022.07.1-554.tar.gz
a46e501a201be6c3c05c0f770c375372 | node-v16.14.0-linux-x64.tar.gz

Maintainer: Isaac Yu (isaacyu1@isaacyu1.com)

[ ] rstudio-desktop (R Statistical IDE)
--- status: ([i] installed, [u] update, [ ] not installed)
[i] R (language and environment for statistical computing)
[u] pandoc-bin (a universal document converter)
[i] yaml-cpp (YAML parser)
[ ] hunspell-en (English hunspell dictionaries)
[ ] yarn (Secure Dependency Management)
[u] apache-ant (Java-based build tool)
[i] zulu-openjdk8 (Open Implementation of JDK)
[i] mathjax2 (Beautiful math in all browsers)
[ ] soci (Database Access Library for C++)
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
To view all potential updates, use the `update` task. Note that this will report differences between SBo and installed packages as updates, irregardless of the actual version number. For example, I have updated locally some of the SlackBuilds I maintain, but have not submitted them yet to SBo:
```
bash-5.1$ sboask updates
--- status: ([u] update; local --> SBo)
[u] DendroPy 4.5.1-1 --> 4.4.0-1
[u] PhyML 3.3.20220408-1 --> 3.3.20200621-1
[u] aliview 1.28-2 --> 1.28-1
[u] apache-ant 1.9.14-1 --> 1.10.12-1
[u] calibre-bin 6.1.0-1 --> 6.2.1-1
[u] datamash 1.8-1 --> 1.7-1
[u] genometools 1.6.2-1 --> 1.6.1-1
[u] hyphy 2.5.40-1 --> 2.5.31-1
[u] mafft 7.490-1 --> 7.475-1
[u] meme-db-motif 12.23-1 --> 12.21-1
[u] meme-suite 5.4.1-1 --> 5.3.3-1
[u] ncbi-blast+ 2.13.0-1 --> 2.11.0-1
[u] nodejs 18.6.0-1 --> 18.7.0-1
[u] openoffice.org 4.1.7_en_US-1 --> 4.1.7-1
[u] pandoc-bin 2.18-1 --> 2.19-1
[u] seaview 5.0.5-1 --> 5.0.4-1
```
If you want to see everything that you have installed from SBo, pass the `installed` task:
```
bash-5.1$ sboask installed
--- status: ([i] installed, [u] update)
[i] BeautifulSoup4
[i] CAFS_divergence
[i] CAPS_coevolution
[i] Data2FCS
[u] DendroPy
[i] EMBASSY
[i] EMBOSS
[i] FCSalyzer
[i] Gblocks
[i] HMMER
[i] IGV
[i] MetaPhlAn2
[i] ORBit2
[i] PDFlib-Lite
[u] PhyML
[i] R
... (snip long list)
[i] zulu-openjdk8
--- status: ([i] installed, [u] update)
```
Finally, to list files of a package, use the `footrpint` task:
```
bash-5.1$ sboask footprint seqkit
FILE LIST:
./
install/
install/slack-desc
usr/
usr/bin/
usr/bin/seqkit
usr/doc/
usr/doc/seqkit-2.2.0/
usr/doc/seqkit-2.2.0/seqkit.SlackBuild
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
  -li,  --sbopkglint        checks produced package
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
import os
import re
import sys

# dirs locations
packages = "/var/lib/pkgtools/packages/"
sbo_repo = "/var/lib/sboutils/15.0/"

# slackbuilds summary
slackbuilds_txt = str(sbo_repo) + "/" + "SLACKBUILDS.TXT"

# check if file or folder exists
def does_it_exist(path):
	if os.path.exists(path):
		return True

# report if file or folder exists
def report_existing(path):
	if does_it_exist(path):
		print("Found: " + path)
	else:
		print("Not found! " + path)

report_existing(packages)
report_existing(sbo_repo)
report_existing(slackbuilds_txt)

# get the SLACKBUILDS.TXT summary
slackbuilds = open(slackbuilds_txt).readlines()

# get installed packages as a list
def installed_packages_list(path):
	pkg_list = []
	for file_name in os.listdir(path):
		pkg_list.append(file_name)
	return pkg_list

# get categories of packages
def packages_categories():
	dict_categories = {}
	for line in slackbuilds:
		if "SLACKBUILD LOCATION" in line:
			description, category, entry = line.rstrip("\n").split("/")
			dict_categories[entry] = category
	return dict_categories

# get packages and their categories
installed_packages_list = installed_packages_list(packages)
packages_categories = packages_categories()

# get full path to file.
# repo (sbo_repo), entry (slackbuild), file (README, info, SlackBuild, slack-desk)
def file_path(repo, entry, file):
	if file == "SlackBuild":
		file = str(entry) + ".SlackBuild"
	elif file == "info":
		file = str(entry) + ".info"
	
	path = str(repo) + str(packages_categories.get(entry)) + "/" + str(entry) + "/" + file
	return path

#print(file_path(sbo_repo, "EMBOSS", "SlackBuild"))

#print(installed_packages_list)
#print(packages_categories["EMBOSS"])

# split the name of a package into parts: name, version, arch, build, tag
def pkg_name_parts(pkg):
	pkg_split = pkg.rsplit("-", 3)
	end = pkg_split[3].split("_", 1)
	build = end[0]
	tag = end[-1]

	# we care about SBo packages
	if tag == "SBo":
		# name, version, arch,...
		pkg_parts = []
		pkg_parts = [pkg_split[0], pkg_split[1], pkg_split[2], build, tag]
		return pkg_parts
	# if the package is not from SBo
	else:
		return pkg_split

# turn entry.info to a dictionary
def source_info(entry):
	info_path = file_path(sbo_repo, entry, "info")
	info_dict = {}
	if os.path.exists(info_path):
		info_file = open(info_path).readlines()
		for line in info_file:
			key, value = line.replace('"', '').replace("\n", "").split("=")
			info_dict[key] = value
		return info_dict

#source_info = source_info("clamtk")
#print(source_info["VERSION"])

# get BUILD version of an entry
def build_version(entry):
	sb_path = file_path(sbo_repo, entry, "SlackBuild")
	if os.path.exists(sb_path):
		sb_file = open(sb_path).readlines()
		for line in sb_file:
			if "BUILD=${BUILD:" in line:
				description, build = line.strip("\n").strip("}").split("BUILD=${BUILD:-")
	return build

#print(build_version("clamtk"))

for pkg in installed_packages_list:
	parts = pkg_name_parts(pkg)
	if parts[-1] == "SBo":
		old = {}
		key = parts[0]
		value = [parts[1], parts[3]]
		old[key] = value
		#print(old)

for pkg in installed_packages_list:
	parts = pkg_name_parts(pkg)
	if parts[-1] == "SBo":
		getinfo = source_info(parts[0])
		#build_version = build_version(pkg)
		#value = [source_info["VERSION"], str(build_version)]

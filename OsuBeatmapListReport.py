#!/usr/local/bin/python2.7
#### @martysama0134 osu-beatmap-list-generator scripts ####
import sys
import os

osuUrlPrefix = "https://osu.ppy.sh/beatmapsets/{}"
osuSearchPrefix = "https://osu.ppy.sh/beatmapsets?q={}"

def getOsuBeatUrl(osuNumber):
	return osuUrlPrefix.format(osuNumber)

def getOsuSearchUrl(osuTitle):
	import urllib
	if sys.version_info[0] < 3:
		return osuSearchPrefix.format(urllib.quote(osuTitle))
	else:
		return osuSearchPrefix.format(urllib.parse.quote(osuTitle))

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def getListFromFolder(osuSongsPath):
	return [os.path.basename(i[0]) for i in walklevel(osuSongsPath) if i[0]!=osuSongsPath]

def getListFromFile(osuListFile):
	""" processing txt files generated with cmd:
		dir /B %localappdata%\osu!\songs > %userprofile%\desktop\osu-list.txt
	"""
	with open(osuListFile) as f1:
		return [dir.strip() for dir in f1.readlines()]

def generateOsuReport(osuOutputReport, osuList):
	with open(osuOutputReport, "w") as f1:
		for dir in dir_list:
			dir = dir.strip()
			if not dir:
				continue
			osuName = dir.split(" ")
			if osuName and osuName[0].isdigit():
				osuNumber = osuName[0]
				osuTitle = " ".join(osuName[1:]) if len(osuName) > 1 else "NoName"
				f1.write("<a href={}>{}</a><br>\n".format(getOsuBeatUrl(osuNumber), osuTitle))
			else:
				osuTitle = " ".join(osuName)
				f1.write("<a href={}>{}</a><br>\n".format(getOsuSearchUrl(osuTitle), osuTitle))
				# print("the folder {} can't be easily tracked".format(dir))


if __name__ == '__main__':
	osuSongsPath = os.path.expandvars(r'%LOCALAPPDATA%\osu!\Songs')
	osuOutputReport = "OsuBeatMapListReport.html"
	osuOutputReport2 = "OsuBeatMapListReport-{}.html"

	dir_list = getListFromFolder(osuSongsPath)
	generateOsuReport(osuOutputReport, dir_list)

	dir_list = getListFromFile("osu-list-marty.txt")
	out_file = osuOutputReport2.format("marty")
	generateOsuReport(out_file, dir_list)

	dir_list = getListFromFile("osu-list-friv.txt")
	out_file = osuOutputReport2.format("friv")
	generateOsuReport(out_file, dir_list)


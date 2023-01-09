#!/usr/bin/python3

from io import BufferedRandom
from mmap import mmap, ALLOCATIONGRANULARITY as PAGE_SIZE, ACCESS_READ
import os
import sys

class OffsetNeeded(Exception):
	pass

class InvalidOffset(Exception):
	pass

class BoomerDetected(Exception):
	pass

#little surprise for boomers who insists using python 2
if sys.version_info.major < 3: raise BoomerDetected("are u serious rn?")

def readLines(fp: BufferedRandom , offset = -1, mem_limit = 10 ** 8, raw=False) -> list: #mem_limit = 100MB
	f_size = os.stat(fp.name).st_size
	offsets = getOffsets(fp)
	chunks = PAGE_SIZE
	if f_size > mem_limit:

		if offset == -1:
			raise OffsetNeeded("file size is greater than provided memory limit, offset is needed")

		if offset % PAGE_SIZE != 0 or offset > f_size:
			raise InvalidOffset("offset must be multiple of page size ({0}) and less or equal to file size ({1})".format(PAGE_SIZE, f_size))

		m = mmap(fp.fileno(), length=chunks, offset=offset)
		data = m.read()
		length = chunks

		while data[-1] != 10:
			length += 1
			m = mmap(fp.fileno(), length=length, offset=offset)
			data = m.read()

		#print(chunks)
		#print(length)

		if raw: return data

		data = data.decode('utf-8').split('\n')
		return data[0:len(data) - 1]

	if raw: return fp.read()

	lines = fp.read().decode('utf-8').split('\n')
	return lines[0:len(lines) - 1]




def getOffsets(fp: BufferedRandom) -> list:
	offsets = [0]
	f_size = os.stat(fp.name).st_size
	offset = PAGE_SIZE
	while offset <= f_size:
		offsets.append(offset)
		offset = nearestOffset(offset)

	return offsets


def nearestOffset(offset: int, fp=None) -> int:

	f_size = os.stat(fp.name).st_size if fp == BufferedRandom else 0

	remainder = offset % PAGE_SIZE
	nearest = offset + PAGE_SIZE - remainder
	nearest = offset if (nearest >= f_size and f_size != 0) else nearest
	return nearest



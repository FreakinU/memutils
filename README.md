# memutils

### a quick python module for processing large files using [mmap](https://docs.python.org/3/library/mmap.html)

part of my random tests with memory managment,  useful to use with ur scripts if ur looking for memory efficiency 

## Testing

### start by writing a junk file

```python
from string import ascii_uppercase
from random import sample
import os

F_NAME = 'large_file'
if os.path.exists(F_NAME): os.remove(F_NAME)

fp = open(F_NAME, 'a')

#not cpu friendly but it the job for a test
for i in range(0, 10 ** 8): # 100MB * 2 
	fp.write("".join(sample(ascii_uppercase, 1)) + "\n")

fp.close()

```

### read the contents from the library and write them to a duplicate file

```python
from memutils import *
import os

original_fp = open('large_file', 'r+b')
offsets = getOffsets(original_fp)
dup = 'duplicate'

if os.path.exists(dup): os.remove(dup)

dup_fp = open(dup, 'a+b')

#not cpu friendly but does the job for a test
for offset in offsets:
	data = readLines(original_fp, offset=offset, raw=True)
	dup_fp.write(data)
	del data


original_fp.close()
dup_fp.close()

```

### compare 

```sh
user@user:~$ md5sum duplicate large_file 
```

## Summed Usage

```python
from memutils import readLines, getOffsets, nearestOffset

fp = open('filename', 'r+b')

#get an assumed next offset depending on the system page size
print(nearestOffset(0x1000)) 

#get next offset of a given file obj
print(nearestOffset(0x1000, fp)) 

#splits a file into parts and reads it without overloading memory
offsets = getOffsets(fp) 

#raw bytes of the 4th offset
print(readLines(fp, offset=offsets[4], raw=True))

#prints lines from first 10 offsets
for i in range(0, 10):

        lines = readLines(fp, offset=offsets[i])
        for line in lines: print(line)
        del lines 
```

## Author: FreakinU
## [License](https://github.com/FreakinU/memutils/blob/main/LICENSE)

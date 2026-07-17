---
title: FFL
description: Fast File Lookup
license: MIT
author: Vahab-Programmer
author_github: Vahab-Programmer
repository: https://github.com/Vahab-Programmer/FFL
keywords:
  - binary-structure
  - file-search
  - file-searcher
  - lookup
  - search
  - trie-data-structure
  - trie-structure
  - vahab-repo
date: 2026-07-11
updated_at: 2026-07-11T15:45:36+00:00
last_sync: 2026-07-11T15:45:36Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 1
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/Vahab-Programmer/FFL/
---

# Fast File Lookup
Simply I Created This Project Because</br>
Windows Explorer Search Bar Just __SUCKS!__</br>
i created this project/library in zig because its really good</br>
Tested in __0.16.0__</br>
you can use this as a package because its a package</br>
i optimized it as much as i could</br>
## Usage
There are Two Executables in 1.0.0</br>
for Indexing we use `FFL-Index`

	FFL-Index <Directory to Index> <output file>
For indexing Program Works better with Higher Privilege</br>
When you index a Path that Path Becomes The Root Directory in program</br>
and for Looking up a File or Directory</br>
we just use `FFL-Lookup`

	FFL-Lookup mycd.ffl
and you get a Simple Console like 

	Directory Counts: 60782
	File Counts: 595716
	Entry Start Point: 0x9c50af
	String:
There are Some Builtin Commands Like
1. __equal__
2. __startswith__
3. __endswith__

for using builtin Commands first you write `?` and your command after it</br>
i cant explain it very well so i will use examples

	?endswith .exe
	?startswith learn_
	?equal learn FFL
`?equal learn FFL` will be two parts
1. ?equal
2. "learn FFL"

i cant explain it better than this ,sorry for any mistakes i made
## Creator
**Author**: **Vahab Programmer**<br>
**Github Page**: **[Vahab-Programmer](https://github.com/Vahab-Programmer)**<br>
**Email**: **vahab.goudarzi.2011@gmail.com**<br>
**Telegram**: **[Vahab Programmer Channel](https://t.me/ProgrammersPersian)**<br>

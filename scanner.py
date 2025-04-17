from os			import access	as osaccess
from os			import path		as ospath
from os			import R_OK
from pathlib	import Path
from typing		import Set
from typing		import List
from typing		import Dict
from typing		import Tuple








def byte_scan(path :str | Path) -> Tuple[bool,str] :

	"""
		Reads "path" file in byte mode and recreates whole message. If any not utf-8 symbol will be
		encountered, it will be substituted with "*" and "broken" flag will be set to True.
		Returns the tuple of "broken" flag and recreated message string. Doesn't handle any
		possible Exceptions, but ensures "path" is accessible file.
	"""

	message	= str()
	broken	= False

	if	isinstance(path, str | Path) and ospath.isfile(path) and osaccess(path, R_OK):

		with open(path, "rb") as file:
			while(B := file.read(1)):

				try:

					match (symbol := B.decode()):

						case "\r":	message += "\n"
						case _:		message += symbol

				except:	message,broken = message + "*",True


		return	broken,	message
	return		True,	message








def sanit_state(path :str | Path) -> Dict[str,int|Set[str]|List[str]] | None :

	"""
		Scans message with "byte_scan" and disassembles it to:
			- raw_lines, unmodified strings obtained after split to lines;
			- air_lines, fully sanitized proper strings of lines split;
			- chunks, set of strings (every word);
			- symbols, all non-whitespace symbols in the message.
		Also maintains a "sanit" state integer that is:
			- zero at start;
			- has first bit set if any proper line "proper" encountered;
			- has second bit set if any proper line "proper" and corresponding "raw" line
			inequality encountered.
		Returns the dictionary of mentioned key-value pairs in case of False value , or a dictionary with
		zero "sanit" and "message" string from "byte_scan" if one encountered not utf-8 symbol.
	"""

	sanit		= 0
	F,message	= byte_scan(path)

	if	not F:

		raw_lines	= [ line for line in message.split("\n") if line and not line.isspace() ]
		air_lines	= list()
		symbols		= set()
		chunks		= set()


		for raw in raw_lines:
			air = list()

			if	(split := raw.split()):
				for word in split:

					current = word.upper()
					air.append(current)
					chunks.add(current)


					for char in current : symbols.add(char)


				air_lines.append(air)
				sanit |= (" ".join(air) != raw) <<1
				sanit |= 1


		return {

			"raw_lines":	raw_lines,
			"air_lines":	air_lines,
			"symbols":		symbols,
			"chunks":		chunks,
			"sanit":		sanit,
		}
	return	{

		"message":	message,
		"sanit":	sanit,
	}








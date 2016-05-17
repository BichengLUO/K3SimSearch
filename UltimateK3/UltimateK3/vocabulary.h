#ifndef VOCABULARY_H
#define VOCABULARY_H

#include <string>
#include <vector>

namespace vocb
{
	typedef struct _word
	{
		std::wstring word;
		std::wstring meaning;
	} word;

	typedef std::vector<word> dict;

	dict load_default_dictionary();
}

#endif
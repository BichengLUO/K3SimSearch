#ifndef VOCABULARY_H
#define VOCABULARY_H

#include <string>
#include <vector>
#include <unordered_map>

namespace vocb
{
	typedef struct _word
	{
		std::wstring word;
		std::wstring meaning;
	} word;

	typedef std::vector<word> dict;
	typedef std::unordered_map<int, int> freq;
	dict load_default_dictionary();
}

#endif
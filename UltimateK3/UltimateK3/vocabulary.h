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
	freq load_default_frequency();
	void save_default_freq(const freq& f);
	bool word_cmp(const word &i, const word &j);
}

#endif
#include "stdafx.h"
#include "vocabulary.h"
#include <fstream>
#include <locale>
#include <codecvt>

namespace vocb
{
	dict load_default_dictionary()
	{
		const std::locale empty_locale = std::locale::empty();
		typedef std::codecvt_utf8<wchar_t> converter_type;
		const converter_type* converter = new converter_type;
		const std::locale utf8_locale = std::locale(empty_locale, converter);

		dict dictionary;
		std::wifstream csv_file("ZYNM3K.csv", std::ifstream::in);
		csv_file.imbue(utf8_locale);
		std::wstring line;
		std::getline(csv_file, line);
		while (std::getline(csv_file, line))
		{
			std::size_t comma = line.find(L",");
			if (comma != std::wstring::npos)
			{
				std::wstring w = line.substr(0, comma);
				std::wstring m = line.substr(comma + 1);
				if (m[0] == L'"') m = m.substr(1, m.length() - 2);
				dictionary.push_back(word{w, m});
			}
		}
		return dictionary;
	}

	freq load_default_frequency()
	{
		freq frequency;
		if (PathFileExists(L"freq.log"))
		{
			std::ifstream freq_file("freq.log", std::ifstream::in);
			int word_id, freq;
			while (freq_file >> word_id >> freq)
				frequency.insert(std::make_pair(word_id, freq));
		}
		return frequency;
	}

	void save_default_freq(const freq& f)
	{
		std::ofstream freq_file("freq.log", std::ofstream::out);
		for (auto it = f.begin(); it != f.end(); it++)
			freq_file << it->first << " " << it->second << " ";
	}
}
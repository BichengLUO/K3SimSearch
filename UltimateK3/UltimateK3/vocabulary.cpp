#include "stdafx.h"
#include "vocabulary.h"
#include <fstream>
#include <locale>
#include <codecvt>
#include <algorithm>

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
				dictionary.push_back(word{ w, m });
			}
		}
		std::sort(dictionary.begin(), dictionary.end(), word_cmp);
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

	bool word_cmp(const word &i, const word &j)
	{
		std::wstring iw = i.word;
		std::wstring jw = j.word;
		std::reverse(iw.begin(), iw.end());
		std::reverse(jw.begin(), jw.end());
		return iw < jw;
	}

	int load_default_page_no()
	{
		int page_no = 0;
		if (PathFileExists(L"page_no.log"))
		{
			std::ifstream page_no_file("page_no.log", std::ifstream::in);
			page_no_file >> page_no;
		}
		return page_no;
	}

	void save_default_page_no(int page_no)
	{
		std::ofstream page_no_file("page_no.log", std::ofstream::out);
		page_no_file << page_no;
	}

	void backup()
	{
		CopyFile(_T("freq.log"), _T("freq.log.bak"), FALSE);
		CopyFile(_T("page_no.log"), _T("page_no.log.bak"), FALSE);
	}
}
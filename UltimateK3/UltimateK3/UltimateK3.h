
// UltimateK3.h : PROJECT_NAME Ӧ�ó������ͷ�ļ�
//

#pragma once

#ifndef __AFXWIN_H__
	#error "�ڰ������ļ�֮ǰ������stdafx.h�������� PCH �ļ�"
#endif

#include "resource.h"		// ������


// CUltimateK3App: 
// �йش����ʵ�֣������ UltimateK3.cpp
//

class CUltimateK3App : public CWinApp
{
public:
	CUltimateK3App();
	GdiplusStartupInput gdiplusStartupInput;
	ULONG_PTR gdiplusToken;

// ��д
public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();

// ʵ��

	DECLARE_MESSAGE_MAP()
};

extern CUltimateK3App theApp;
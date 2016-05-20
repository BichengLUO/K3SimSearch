
// UltimateK3Dlg.cpp : 实现文件
//

#include "stdafx.h"
#include "UltimateK3.h"
#include "UltimateK3Dlg.h"
#include "afxdialogex.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// 用于应用程序“关于”菜单项的 CAboutDlg 对话框

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CUltimateK3Dlg 对话框



CUltimateK3Dlg::CUltimateK3Dlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(CUltimateK3Dlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CUltimateK3Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CUltimateK3Dlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_WM_ERASEBKGND()
	ON_WM_MOUSEMOVE()
	ON_WM_LBUTTONDOWN()
	ON_WM_RBUTTONDOWN()
	ON_WM_CLOSE()
//	ON_BN_CLICKED(IDC_CHECK_SHOW_DEFINITIONS, &CUltimateK3Dlg::OnBnClickedCheckShowDefinitions)
END_MESSAGE_MAP()


// CUltimateK3Dlg 消息处理程序

BOOL CUltimateK3Dlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 将“关于...”菜单项添加到系统菜单中。

	// IDM_ABOUTBOX 必须在系统命令范围内。
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	// TODO:  在此添加额外的初始化代码
	dictionary = vocb::load_default_dictionary();
	frequency = vocb::load_default_frequency();
	top_margin = 60;
	left_margin = 60;
	current_page = 0;
	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}

void CUltimateK3Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。  对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void CUltimateK3Dlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CRect rect;
		GetClientRect(&rect);
		Pen pen_black(Color::Black);
		Pen pen_gray(Color::Gray, 2);
		SolidBrush brush_white(Color::White);
		SolidBrush brush_gray(Color::Gray);
		SolidBrush brush_black(Color::Black);
		SolidBrush brush_blue(Color::Blue);
		SolidBrush brush_back(Color::MakeARGB(255, 240, 240, 240));

		Bitmap pMemBitmap(rect.Width(), rect.Height());
		Graphics* pMemGraphics = Graphics::FromImage(&pMemBitmap);
		pMemGraphics->SetSmoothingMode(SmoothingMode::SmoothingModeAntiAlias);
		pMemGraphics->FillRectangle(&brush_back, 0, 0, rect.Width(), rect.Height());
		pMemGraphics->FillRectangle(&brush_white, 0, 0, rect.Width(), rect.Height() - 30);

		CPaintDC dc(this);
		Graphics graphics(dc.m_hDC);

		int cell_height = (rect.Height() - 2 * top_margin) / 10.0;
		int cell_width = (rect.Width() - 2 * left_margin) / 10.0;

		Brush *left_brush = on_left ? &brush_black : &brush_gray;
		Brush *right_brush = on_right ? &brush_black : &brush_gray;

		pMemGraphics->FillEllipse(left_brush, -40, (rect.Height() - 120) / 2.0, 80, 120);
		pMemGraphics->FillEllipse(right_brush, rect.Width() - 40, (rect.Height() - 120) / 2.0, 80, 120);
		draw_string(pMemGraphics, L"←",
			0, (rect.Height() - 40) / 2.0 + 5, 40, 40,
			15, &brush_white);
		draw_string(pMemGraphics, L"→",
			rect.Width() - 40, (rect.Height() - 40) / 2.0 + 5, 40, 40,
			15, &brush_white);

		wchar_t unit_title[128];
		wsprintf(unit_title, L"List %d", current_page + 1);
		draw_string(pMemGraphics, unit_title,
			(rect.Width() - 300) / 2.0, 20, 300, 40,
			15, &brush_black);
		std::wstring current_w;
		std::wstring current_m;
		int m_y = rect.Height() - 50;
		for (int i = 0; i < 100 && current_page * 100 + i < dictionary.size(); i++)
		{
			int row = i / 10;
			int col = i % 10;
			int word_id = current_page * 100 + i;
			Brush *font_brush = &brush_black;

			std::wstring w = dictionary[current_page * 100 + i].word;
			std::wstring m = dictionary[current_page * 100 + i].meaning;
			wchar_t *font_name = L"Microsoft Yahei";
			if (frequency.find(word_id) != frequency.end())
			{
				int freq = frequency[word_id];
				freq = freq > 20 ? 20 : freq;
				SolidBrush freq_brush(Color::MakeARGB(255, 250, 255 - freq * 6, 255 - freq * 12));
				pMemGraphics->FillRectangle(&freq_brush,
					left_margin + col * cell_width, top_margin + row * cell_height, cell_width, cell_height);
				wchar_t freq_count[128];
				wsprintf(freq_count, L"%d", frequency[word_id]);
				SolidBrush inv_freq_brush(Color::MakeARGB(255, 5, freq * 6, freq * 12));
				font_name = L"Arial Black";
				draw_string(pMemGraphics, freq_count,
					left_margin + col * cell_width, top_margin + (row + 1) * cell_height - 15, cell_width, 15,
					9, &inv_freq_brush, font_name);
			}
			if (row == current_row && col == current_col)
			{
				pMemGraphics->FillRectangle(&brush_blue,
					left_margin + col * cell_width, top_margin + row * cell_height, cell_width, cell_height);
				font_brush = &brush_white;
				current_w = w;
				current_m = m;
				if (current_row >= 5) m_y = 5;
			}
			int font_size = 11;
			if (w.length() >= 12)
				font_size = 9;
			else if (w.length() >= 10)
				font_size = 10;
			else if (w.length() <= 5)
				font_size = 12;
			draw_string(pMemGraphics, w.c_str(),
				left_margin + col * cell_width, 15 + top_margin + row * cell_height, cell_width, cell_height - 15,
				font_size, font_brush, font_name);
		}

		for (int i = 0; i < 11; i++)
		{
			pMemGraphics->DrawLine(&pen_gray, left_margin, top_margin + i * cell_height,
				left_margin + 10 * cell_width, top_margin + i * cell_height);
			pMemGraphics->DrawLine(&pen_gray, left_margin + i * cell_width, top_margin,
				left_margin + i * cell_width, top_margin + 10 * cell_height);
		}

		if (((CButton*)GetDlgItem(IDC_CHECK_SHOW_DEFINITIONS))->GetCheck())
			draw_string(pMemGraphics, current_m.c_str(),
			(rect.Width() - 800) / 2.0, m_y, 800, 30,
			10, &brush_gray);

		delete pMemGraphics;
		graphics.DrawImage(&pMemBitmap, 0, 0);
	}
}

void CUltimateK3Dlg::draw_string(Graphics* pMemGraphics, const wchar_t *str,
	int x, int y, int width, int height,
	int font_size, Brush *brush, const wchar_t *font_name)
{
	// Initialize arguments.
	Gdiplus::Font myFont(font_name, font_size);
	StringFormat format;
	format.SetAlignment(StringAlignmentCenter);

	// Draw string.
	pMemGraphics->DrawString(
		str,
		wcslen(str),
		&myFont,
		RectF(x, y, width, height),
		&format,
		brush);
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR CUltimateK3Dlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



BOOL CUltimateK3Dlg::OnEraseBkgnd(CDC* pDC)
{
	// TODO:  在此添加消息处理程序代码和/或调用默认值
	return TRUE;
}


void CUltimateK3Dlg::OnMouseMove(UINT nFlags, CPoint point)
{
	// TODO:  在此添加消息处理程序代码和/或调用默认值
	CRect rect;
	GetClientRect(&rect);
	CRect voc_rect(left_margin, top_margin, rect.Width() - left_margin, rect.Height() - top_margin);
	on_voc = voc_rect.PtInRect(point);
	if (on_voc)
	{
		int cell_height = (rect.Height() - 2 * top_margin) / 10.0;
		int cell_width = (rect.Width() - 2 * left_margin) / 10.0;
		current_row = (point.y - top_margin) / cell_height;
		current_col = (point.x - left_margin) / cell_width;
	}
	else current_row = current_col = -1;

	CRect left_page_rec(0, (rect.Height() - 120) / 2.0, 40, (rect.Height() - 120) / 2.0 + 120);
	CRect right_page_rec(rect.Width() - 40, (rect.Height() - 120) / 2.0, rect.Width(), (rect.Height() - 120) / 2.0 + 120);
	on_left = left_page_rec.PtInRect(point);
	on_right = right_page_rec.PtInRect(point);
	rect.bottom -= 30;
	InvalidateRect(rect);
	CDialogEx::OnMouseMove(nFlags, point);
}


void CUltimateK3Dlg::OnLButtonDown(UINT nFlags, CPoint point)
{
	// TODO:  在此添加消息处理程序代码和/或调用默认值
	CRect rect;
	GetClientRect(&rect);
	if (on_left)
		current_page = current_page - 1 < 0 ? 0 : current_page - 1;
	else if (on_right)
		current_page = (current_page + 1) * 100 >= dictionary.size() ? current_page : current_page + 1;
	if (on_voc)
	{
		int word_id = current_page * 100 + current_row * 10 + current_col;
		if (frequency.find(word_id) == frequency.end())
			frequency.insert(std::make_pair(word_id, 1));
		else
			frequency[word_id]++;
	}
	rect.bottom -= 30;
	InvalidateRect(rect);
	CDialogEx::OnLButtonDown(nFlags, point);
}


void CUltimateK3Dlg::OnRButtonDown(UINT nFlags, CPoint point)
{
	// TODO:  在此添加消息处理程序代码和/或调用默认值
	CRect rect;
	GetClientRect(&rect);
	if (on_voc)
	{
		int word_id = current_page * 100 + current_row * 10 + current_col;
		if (frequency.find(word_id) != frequency.end())
			frequency.erase(word_id);
	}
	rect.bottom -= 30;
	InvalidateRect(rect);
	CDialogEx::OnRButtonDown(nFlags, point);
}


void CUltimateK3Dlg::OnClose()
{
	// TODO:  在此添加消息处理程序代码和/或调用默认值
	vocb::save_default_freq(frequency);
	CDialogEx::OnClose();
}


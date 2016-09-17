
// UltimateK3Dlg.h : ͷ�ļ�
//

#pragma once
#include "vocabulary.h"

// CUltimateK3Dlg �Ի���
class CUltimateK3Dlg : public CDialogEx
{
// ����
public:
	CUltimateK3Dlg(CWnd* pParent = NULL);	// ��׼���캯��

// �Ի�������
	enum { IDD = IDD_ULTIMATEK3_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV ֧��
	vocb::dict dictionary;
	vocb::freq frequency;
	int current_page;
	int current_row;
	int current_col;
	int top_margin;
	int left_margin;
	bool on_voc;
	bool on_left;
	bool on_right;
	double seconds;
	int timer;

// ʵ��
protected:
	HICON m_hIcon;

	// ���ɵ���Ϣӳ�亯��
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	void draw_string(Graphics* pMemGraphics, const wchar_t *str,
		int x, int y, int width, int height,
		int font_size, Brush *brush, const wchar_t *font_name = L"Microsoft Yahei");
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnRButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnClose();
//	afx_msg void OnBnClickedCheckShowDefinitions();
	afx_msg void OnTimer(UINT_PTR nIDEvent);
};

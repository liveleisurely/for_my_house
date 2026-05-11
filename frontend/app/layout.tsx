import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'For My House',
  description: '풍무 해링턴 74A 리스크 모니터링 대시보드'
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}

import type { Metadata } from "next";

import "@/app/globals.css";

export const metadata: Metadata = {
  title: "MeetTruth Agent",
  description: "Meeting authenticity inspection console for playback-first risk analysis.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}

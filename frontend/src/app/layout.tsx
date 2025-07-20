import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ECSS Navigator - AI-Powered Space Standards Search",
  description: "Advanced RAG technology for searching European Cooperation for Space Standardization (ECSS) documents with AI precision",
  keywords: "ECSS, space standards, aerospace, engineering standards, space engineering, AI search, RAG technology",
  authors: [{ name: "ECSS Navigator Team" }],
  openGraph: {
    title: "ECSS Navigator - AI-Powered Space Standards Search",
    description: "Advanced RAG technology for searching European Cooperation for Space Standardization (ECSS) documents with AI precision",
    type: "website",
    url: "https://ecss-hunt.vercel.app",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}

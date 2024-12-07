import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Eye Fleet - Modern Fleet Management",
  description: "Professional fleet management platform for tracking vehicles, maintenance, and operations",
  icons: {
    icon: [
      {
        url: "/eye_fleet_logo.png",
        sizes: "32x32",
        type: "image/png"
      },
      {
        url: "/eye_fleet_logo.png",
        sizes: "16x16",
        type: "image/png"
      }
    ],
    apple: [
      {
        url: "/eye_fleet_logo.png",
        sizes: "180x180",
        type: "image/png"
      }
    ]
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Eye Fleet"
  },
  applicationName: "Eye Fleet",
  keywords: ["fleet management", "vehicle tracking", "maintenance", "operations"],
  authors: [{ name: "Eye Fleet Team" }],
  viewport: "width=device-width, initial-scale=1",
  themeColor: "#000000",
  manifest: "/manifest.json"
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import { Orbitron, Rajdhani } from "next/font/google";
import "./globals.css";
import DashboardNav from "@/components/DashboardNav";

// 🤖 Robotic Futuristic Font
const orbitron = Orbitron({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
  variable: "--font-heading",
  display: "swap",
});

// 🤖 Clean Tech Body Font
const rajdhani = Rajdhani({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-body",
  display: "swap",
});

export const metadata: Metadata = {
  title: "🤖 Campus AI - Robotic Event Management System",
  description:
    "AI-Powered Campus Event Management. Advanced ML-driven poster analysis, automated attendance tracking, and intelligent OD management. The future of educational technology.",
  keywords: [
    "AI campus management",
    "robotic event system",
    "ML poster analysis",
    "automated attendance",
    "AI education tech",
    "machine learning events",
    "smart campus",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth dark">
      <body
        className={`${orbitron.variable} ${rajdhani.variable} antialiased min-h-screen`}
      >
        <DashboardNav />
        <div className="pt-16 relative z-10">
          {children}
        </div>
        
        {/* 🤖 Cyber Grid Overlay */}
        <div className="fixed inset-0 pointer-events-none z-0 opacity-30">
          <div className="absolute inset-0" style={{
            backgroundImage: 'linear-gradient(rgba(0, 229, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 229, 255, 0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px'
          }}></div>
        </div>
      </body>
    </html>
  );
}

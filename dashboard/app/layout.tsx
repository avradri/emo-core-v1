// dashboard/app/layout.tsx
import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Emergent Mind Observatory – DestinE Dual-Twin",
  description:
    "UIA-flavoured cognitive vital signs over DestinE climate scenarios."
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="emo-body">
        <div className="emo-shell">
          {children}
        </div>
      </body>
    </html>
  );
}

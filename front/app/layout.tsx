//signforms/src/app/layout.tsx

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

import AuthSession from './Provider'
import LoginButton from './pages/login'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthSession>
          <div className="h-[48px] bg-black flex items-center">
            <ul className="ml-auto mr-5">
              <li><LoginButton></LoginButton></li>

            </ul>
          </div>
          {children}
        </AuthSession>
      </body>
    </html>
  )
}

import { Outlet } from "react-router"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { ThemeToggle } from "@/components/theme-toggle"
import { TooltipProvider } from "@/components/ui/tooltip"

export default function RootLayout({ onNewChat }) {
  return (
    <TooltipProvider>
      <SidebarProvider>
        <div className="flex min-h-screen w-full bg-background">
          <AppSidebar onNewChat={onNewChat} />
          <SidebarInset className="flex flex-col">
            <header className="flex h-14 items-center justify-between border-b px-4 lg:px-6 shrink-0">
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-semibold tracking-tight">AviAI</h1>
              </div>
              <ThemeToggle />
            </header>
            <main className="flex-1 overflow-hidden">
              <Outlet />
            </main>
          </SidebarInset>
        </div>
      </SidebarProvider>
    </TooltipProvider>
  )
}

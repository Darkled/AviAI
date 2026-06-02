import { MessageSquare, Plus, History } from "lucide-react"
import { Link } from "react-router"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
  useSidebar,
} from "@/components/ui/sidebar"
import { Button } from "@/components/ui/button"

export function AppSidebar({ onNewChat }) {
  const { state } = useSidebar()
  const isCollapsed = state === "collapsed"

  // Mock chat history
  const history = [
    { id: 1, title: "Fleet Capacity Analysis" },
    { id: 2, title: "Fuel Efficiency Comparison" },
    { id: 3, title: "Maintenance Status Report" },
    { id: 4, title: "Boeing 787 Performance" },
  ]

  return (
    <Sidebar variant="sidebar" collapsible="icon" className="border-r">
      <SidebarHeader className="p-4">
        <Button 
          className={`w-full gap-2 ${isCollapsed ? "justify-center px-0" : "justify-start"}`}
          variant="outline"
          onClick={onNewChat}
          title={isCollapsed ? "New Chat" : undefined}
        >
          <Plus className="h-4 w-4" />
          {!isCollapsed && <span>New Chat</span>}
        </Button>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Recent Chats</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {history.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton asChild>
                    <Link to={`/chat/${item.id}`} className="flex items-center gap-2">
                      <MessageSquare className="h-4 w-4" />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="p-4 border-t">
        <div className={`flex items-center gap-2 px-2 py-1.5 text-sm text-muted-foreground ${isCollapsed ? "justify-center" : ""}`}>
          <History className="h-4 w-4" />
          {!isCollapsed && <span>History version 1.0</span>}
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}

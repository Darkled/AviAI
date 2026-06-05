import { MessageSquare, Plus, History, Trash2 } from "lucide-react"
import { Link, useNavigate, useParams } from "react-router"
import { useState, useEffect } from "react"
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
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"

export function AppSidebar({ onNewChat }) {
  const { state } = useSidebar()
  const isCollapsed = state === "collapsed"
  const [history, setHistory] = useState([])
  const [chatToDelete, setChatToDelete] = useState(null)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const { chatId: currentChatId } = useParams()
  const navigate = useNavigate()

  const fetchHistory = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/chats")
      if (response.ok) {
        const data = await response.json()
        setHistory(data)
      }
    } catch (error) {
      console.error("Failed to fetch history:", error)
    }
  }

  useEffect(() => {
    fetchHistory()
    
    // Refresh history periodically or on specific events
    const interval = setInterval(fetchHistory, 10000)
    return () => clearInterval(interval)
  }, [])

  const handleDeleteClick = (e, id) => {
    e.preventDefault()
    e.stopPropagation()
    setChatToDelete(id)
    setIsDeleteDialogOpen(true)
  }

  const confirmDelete = async () => {
    if (!chatToDelete) return

    try {
      const response = await fetch(`http://localhost:8000/api/chats/${chatToDelete}`, {
        method: "DELETE",
      })
      if (response.ok) {
        fetchHistory()
        if (currentChatId === chatToDelete.toString()) {
          onNewChat()
        }
      }
    } catch (error) {
      console.error("Failed to delete chat:", error)
    } finally {
      setIsDeleteDialogOpen(false)
      setChatToDelete(null)
    }
  }

  return (
    <>
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
                    <div className="group flex items-center w-full pr-2">
                      <SidebarMenuButton asChild isActive={currentChatId === item.id.toString()}>
                        <Link to={`/chat/${item.id}`} className="flex items-center gap-2 overflow-hidden">
                          <MessageSquare className="h-4 w-4 shrink-0" />
                          <span className="truncate">{item.title}</span>
                        </Link>
                      </SidebarMenuButton>
                      {!isCollapsed && (
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7 opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={(e) => handleDeleteClick(e, item.id)}
                        >
                          <Trash2 className="h-3.5 w-3.5 text-muted-foreground hover:text-destructive" />
                        </Button>
                      )}
                    </div>
                  </SidebarMenuItem>
                ))}
                {history.length === 0 && !isCollapsed && (
                  <div className="px-4 py-2 text-xs text-muted-foreground">
                    No chats yet
                  </div>
                )}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
        <SidebarFooter className="p-4 border-t">
          <div className={`flex items-center gap-2 px-2 py-1.5 text-sm text-muted-foreground ${isCollapsed ? "justify-center" : ""}`}>
            <History className="h-4 w-4" />
            {!isCollapsed && <span>History version 1.1</span>}
          </div>
        </SidebarFooter>
      </Sidebar>

      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete your
              chat history and remove the data from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Delete Chat
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}

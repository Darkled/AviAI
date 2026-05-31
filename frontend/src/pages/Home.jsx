import { useState, useRef, useEffect } from "react"
import { SendHorizontal, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card } from "@/components/ui/card"

export default function Home() {
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState([])
  const textareaRef = useRef(null)
  const scrollAreaRef = useRef(null)

  // Auto-expand textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "inherit"
      const scrollHeight = textareaRef.current.scrollHeight
      textareaRef.current.style.height = `${scrollHeight}px`
    }
  }, [input])

  const handleSend = () => {
    if (!input.trim()) return
    setMessages([...messages, { role: "user", content: input }])
    setInput("")
    // Mock response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: "assistant", 
        content: "I'm a placeholder AI response. How can I help you today?" 
      }])
    }, 1000)
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto px-4 md:px-0">
      <ScrollArea className="flex-1 py-6 pr-4" ref={scrollAreaRef}>
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-1000">
            <div className="bg-primary/10 p-4 rounded-full">
              <Sparkles className="h-10 w-10 text-primary" />
            </div>
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tight">Welcome to AI Chat</h2>
              <p className="text-muted-foreground max-w-[420px]">
                Start a conversation to see how I can help you with your tasks, 
                answer your questions, or just chat.
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg mt-8">
              {["Explain quantum physics", "Write a poem about rain", "How to make a pizza?", "Refactor this code"].map((suggestion) => (
                <Button 
                  key={suggestion} 
                  variant="outline" 
                  className="justify-start font-normal h-auto py-3 px-4 text-sm rounded-xl border-muted"
                  onClick={() => setInput(suggestion)}
                >
                  {suggestion}
                </Button>
              ))}
            </div>
          </div>
        ) : (
          <div className="space-y-6 pb-4">
            {messages.map((message, i) => (
              <div
                key={i}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <Card className={`max-w-[80%] px-4 py-3 rounded-2xl shadow-none ${
                  message.role === "user" 
                    ? "bg-primary text-primary-foreground border-transparent" 
                    : "bg-muted/50 border-border"
                }`}>
                  <p className="whitespace-pre-wrap leading-relaxed">
                    {message.content}
                  </p>
                </Card>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>

      <div className="py-6 shrink-0">
        <div className="relative flex items-end gap-2 bg-background p-2 rounded-2xl border border-border focus-within:border-primary/50 transition-colors">
          <Textarea
            ref={textareaRef}
            tabIndex={0}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Send a message..."
            className="min-h-[44px] max-h-[200px] w-full resize-none bg-background border-0 focus-visible:ring-0 focus-visible:ring-offset-0 px-3 py-3"
          />
          <Button 
            size="icon" 
            className="rounded-xl h-11 w-11 shrink-0" 
            disabled={!input.trim()}
            onClick={handleSend}
          >
            <SendHorizontal className="h-5 w-5" />
          </Button>
        </div>
        <p className="text-[10px] text-center text-muted-foreground mt-2 px-4">
          AI can make mistakes. Consider checking important information.
        </p>
      </div>
    </div>
  )
}

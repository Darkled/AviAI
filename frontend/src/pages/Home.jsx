import { useState, useRef, useEffect } from "react"
import { useParams, useNavigate } from "react-router"
import { SendHorizontal, Sparkles } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card } from "@/components/ui/card"

export default function Home({ messages, setMessages }) {
  const { chatId } = useParams()
  const navigate = useNavigate()
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const textareaRef = useRef(null)
  const scrollAreaRef = useRef(null)

  // Load chat messages if chatId exists
  useEffect(() => {
    if (chatId) {
      const fetchMessages = async () => {
        try {
          const response = await fetch(`http://localhost:8000/api/chats/${chatId}/messages`)
          if (response.ok) {
            const data = await response.json()
            setMessages(data)
          } else {
            console.error("Failed to fetch messages")
            navigate("/")
          }
        } catch (error) {
          console.error("Error fetching messages:", error)
        }
      }
      fetchMessages()
    } else {
      setMessages([])
    }
  }, [chatId, navigate, setMessages])

  // Auto-expand textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "inherit"
      const scrollHeight = textareaRef.current.scrollHeight
      textareaRef.current.style.height = `${scrollHeight}px`
    }
  }, [input])

  // Auto-scroll to bottom
  useEffect(() => {
    const viewport = scrollAreaRef.current?.querySelector('[data-radix-scroll-area-viewport]')
    if (viewport) {
      viewport.scrollTop = viewport.scrollHeight
    }
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const cleanedInput = input
      .split("\n")
      .map((line) => line.trimEnd())
      .filter((line) => line !== "")
      .join("\n")
      .trim()

    if (!cleanedInput) return

    const userMessage = { role: "user", content: cleanedInput }
    const initialMessages = [...messages, userMessage]
    setMessages(initialMessages)
    setInput("")
    setIsLoading(true)

    // Add a placeholder for the assistant response
    const assistantMessageIndex = initialMessages.length
    setMessages(prev => [...prev, { role: "assistant", content: "" }])

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: cleanedInput,
          chat_id: chatId ? parseInt(chatId) : null
        }),
      })

      if (!response.ok) throw new Error("Failed to connect to AI")

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let assistantContent = ""

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        
        // Check for metadata at the end of the stream
        if (chunk.includes("[METADATA]")) {
          const parts = chunk.split("[METADATA]")
          assistantContent += parts[0]
          
          try {
            const metadata = JSON.parse(parts[1])
            if (!chatId && metadata.chat_id) {
              // Redirect to the new chat URL without clearing messages
              navigate(`/chat/${metadata.chat_id}`, { replace: true })
            }
          } catch (e) {
            console.error("Failed to parse metadata:", e)
          }
        } else {
          assistantContent += chunk
        }

        // Update the assistant message in the state
        setMessages(prev => {
          const newMessages = [...prev]
          newMessages[assistantMessageIndex] = {
            ...newMessages[assistantMessageIndex],
            content: assistantContent,
          }
          return newMessages
        })
      }
    } catch (error) {
      console.error("Streaming error:", error)
      setMessages(prev => {
        const newMessages = [...prev]
        newMessages[assistantMessageIndex] = {
          ...newMessages[assistantMessageIndex],
          content: "Sorry, I encountered an error. Please try again later.",
        }
        return newMessages
      })
    } finally {
      setIsLoading(false)
    }
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
              <h2 className="text-3xl font-bold tracking-tight">Airline Management AI</h2>
              <p className="text-muted-foreground max-w-[420px]">
                Welcome! I can help you analyze your aircraft fleet, compare technical specs, 
                and manage your airline's operational data.
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg mt-8">
              {[
                "Highest passenger capacity?",
                "Boeing vs Airbus fuel burn",
                "Fleet status summary",
                "Aircraft with range > 5000km"
              ].map((suggestion) => (
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
                <Card className={`max-w-[85%] px-4 py-3 rounded-2xl shadow-none ${
                  message.role === "user" 
                    ? "bg-primary text-primary-foreground border-transparent" 
                    : "bg-muted/50 border-border"
                }`}>
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    {message.role === "assistant" ? (
                      <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        components={{
                          table: ({node, ...props}) => (
                            <div className="overflow-x-auto my-4 border rounded-lg">
                              <table className="min-w-full divide-y divide-border" {...props} />
                            </div>
                          ),
                          th: ({node, ...props}) => (
                            <th className="px-4 py-2 bg-muted font-semibold text-left" {...props} />
                          ),
                          td: ({node, ...props}) => (
                            <td className="px-4 py-2 border-t border-border" {...props} />
                          )
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    ) : (
                      <p className="whitespace-pre-wrap leading-relaxed">
                        {message.content}
                      </p>
                    )}
                  </div>
                </Card>
              </div>
            ))}
            {isLoading && !messages[messages.length - 1]?.content && (
              <div className="flex justify-start">
                <Card className="max-w-[85%] px-4 py-3 rounded-2xl shadow-none bg-muted/50 border-border italic text-muted-foreground animate-pulse">
                  Thinking...
                </Card>
              </div>
            )}
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
            disabled={isLoading}
            className="min-h-[44px] max-h-[200px] w-full resize-none bg-background border-0 focus-visible:ring-0 focus-visible:ring-offset-0 px-3 py-3"
          />
          <Button 
            size="icon" 
            className="rounded-xl h-11 w-11 shrink-0" 
            disabled={!input.trim() || isLoading}
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

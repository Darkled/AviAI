import { BrowserRouter, Routes, Route, useNavigate } from "react-router"
import { useState } from "react"
import RootLayout from "@/layouts/RootLayout"
import Home from "@/pages/Home"
import NotFound from "@/pages/NotFound"
import { ThemeProvider } from "@/components/theme-provider"

function AppContent() {
  const [messages, setMessages] = useState([])
  const navigate = useNavigate()

  const startNewChat = () => {
    setMessages([])
    navigate("/")
  }

  return (
    <Routes>
      <Route element={<RootLayout onNewChat={startNewChat} />}>
        <Route path="/" element={<Home messages={messages} setMessages={setMessages} />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="ui-theme">
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App

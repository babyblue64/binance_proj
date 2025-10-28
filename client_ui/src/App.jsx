import { useState } from 'react'
import TradeTicker from './TradeTicker'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <TradeTicker />
    </>
  )
}

export default App

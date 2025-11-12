import { useState } from 'react'
import './HelloButton.css'

function HelloButton({ onClick, loading }) {
  const [isClicked, setIsClicked] = useState(false)

  const handleClick = async () => {
    setIsClicked(true)
    await onClick()
    setTimeout(() => setIsClicked(false), 300)
  }

  return (
    <button
      className={`hello-button ${isClicked ? 'clicked' : ''} ${loading ? 'loading' : ''}`}
      onClick={handleClick}
      disabled={loading}
      aria-label="Get message from backend"
      aria-busy={loading}
    >
      {loading ? (
        <>
          <span className="spinner"></span>
          <span>Loading...</span>
        </>
      ) : (
        'Get Message from Backend'
      )}
    </button>
  )
}

export default HelloButton

import PropTypes from 'prop-types'
import './MessageDisplay.css'

const MessageDisplay = ({ message, timestamp, className = '' }) => {
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return new Date().toLocaleString()
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div 
      className={`message-display ${className}`}
      role="region"
      aria-labelledby="message-title"
      aria-live="polite"
    >
      <div className="message-icon" aria-hidden="true">
        ✅
      </div>
      <div className="message-content">
        <h3 id="message-title" className="message-title">
          Message from Backend
        </h3>
        <p className="message-text">{message}</p>
        <p className="message-timestamp">
          Received at: {formatTimestamp(timestamp)}
        </p>
      </div>
    </div>
  )
}

MessageDisplay.propTypes = {
  message: PropTypes.string.isRequired,
  timestamp: PropTypes.string,
  className: PropTypes.string
}

export default MessageDisplay
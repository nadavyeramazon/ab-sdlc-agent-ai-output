import PropTypes from 'prop-types'
import './MessageDisplay.css'

const MessageDisplay = ({ message, className = '' }) => {
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
      </div>
    </div>
  )
}

MessageDisplay.propTypes = {
  message: PropTypes.string.isRequired,
  className: PropTypes.string
}

export default MessageDisplay
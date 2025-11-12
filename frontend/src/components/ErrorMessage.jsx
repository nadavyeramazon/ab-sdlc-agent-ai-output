import PropTypes from 'prop-types'
import './ErrorMessage.css'

const ErrorMessage = ({ message, onRetry, id, className = '' }) => {
  return (
    <div 
      id={id}
      className={`error-message ${className}`} 
      role="alert"
      aria-live="polite"
    >
      <div className="error-content">
        <div className="error-icon" aria-hidden="true">
          ⚠️
        </div>
        <div className="error-text">
          <p className="error-title">Something went wrong</p>
          <p className="error-description">{message}</p>
        </div>
      </div>
      {onRetry && (
        <button
          className="error-retry-btn"
          onClick={onRetry}
          type="button"
          aria-label="Retry the previous action"
        >
          Try Again
        </button>
      )}
    </div>
  )
}

ErrorMessage.propTypes = {
  message: PropTypes.string.isRequired,
  onRetry: PropTypes.func,
  id: PropTypes.string,
  className: PropTypes.string
}

export default ErrorMessage
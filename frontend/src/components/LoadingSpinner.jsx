import PropTypes from 'prop-types'
import './LoadingSpinner.css'

const LoadingSpinner = ({ size = 'md', color = 'primary', className = '' }) => {
  return (
    <div 
      className={`loading-spinner loading-spinner--${size} loading-spinner--${color} ${className}`}
      role="status"
      aria-label="Loading"
    >
      <div className="spinner-ring">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
      <span className="sr-only">Loading...</span>
    </div>
  )
}

LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['xs', 'sm', 'md', 'lg', 'xl']),
  color: PropTypes.oneOf(['primary', 'secondary', 'white']),
  className: PropTypes.string
}

export default LoadingSpinner
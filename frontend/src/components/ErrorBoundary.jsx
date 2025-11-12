import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #1e8449 0%, #27ae60 50%, #2ecc71 100%)',
            padding: '2rem',
          }}
        >
          <div
            style={{
              background: 'white',
              borderRadius: '12px',
              padding: '2.5rem',
              maxWidth: '600px',
              width: '100%',
              boxShadow: '0 10px 15px rgba(0, 0, 0, 0.2)',
            }}
          >
            <h1
              style={{
                color: '#e74c3c',
                fontSize: '2rem',
                marginBottom: '1rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
              }}
            >
              <svg
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="currentColor"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z"
                  clipRule="evenodd"
                />
              </svg>
              Something went wrong
            </h1>
            <p
              style={{
                color: '#555',
                fontSize: '1.125rem',
                marginBottom: '1.5rem',
                lineHeight: '1.6',
              }}
            >
              We're sorry, but something unexpected happened. Please try refreshing the page.
            </p>
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details
                style={{
                  background: '#f8f9fa',
                  padding: '1rem',
                  borderRadius: '8px',
                  marginBottom: '1.5rem',
                  fontSize: '0.875rem',
                  color: '#333',
                }}
              >
                <summary
                  style={{
                    cursor: 'pointer',
                    fontWeight: '600',
                    marginBottom: '0.5rem',
                  }}
                >
                  Error Details (Development Only)
                </summary>
                <pre
                  style={{
                    overflow: 'auto',
                    marginTop: '0.5rem',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}
                >
                  {this.state.error.toString()}
                  {this.state.errorInfo && this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}
            <button
              onClick={() => window.location.reload()}
              style={{
                background: 'linear-gradient(135deg, #27ae60, #2ecc71)',
                color: 'white',
                border: 'none',
                padding: '0.875rem 1.75rem',
                fontSize: '1rem',
                fontWeight: '600',
                borderRadius: '8px',
                cursor: 'pointer',
                width: '100%',
                transition: 'all 0.3s ease',
              }}
              onMouseOver={(e) => {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
              }}
              onMouseOut={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = 'none';
              }}
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

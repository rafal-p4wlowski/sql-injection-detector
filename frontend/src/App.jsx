import { useState } from 'react';

function App() {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [statusMessage, setStatusMessage] = useState(null);
  const [statusType, setStatusType] = useState(null); // 'success', 'warning', 'error' (statusy)
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStatusMessage(null);
    setStatusType(null);

    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ login, password }),
      });

      const data = await response.json();

      if (response.status === 200) {
        setStatusType('success');
        setStatusMessage(data.message);
      } else if (response.status === 401) {
        setStatusType('warning');
        setStatusMessage(data.message);
      } else if (response.status === 403) {
        setStatusType('error');
        setStatusMessage('Uwaga! System zablokowal probe ataku SQL Injection!');
      } else {
        setStatusType('warning');
        setStatusMessage('Wystapil nieoczekiwany blad serwera.');
      }
    } catch (error) {
      console.error('Blad podczas logowania:', error);
      setStatusType('error');
      setStatusMessage('Blad polaczenia z serwerem. Upewnij sie, ze backend dziala.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="p-8">
            <h2 className="text-3xl font-extrabold text-center text-gray-800 mb-2">Panel logowania</h2>
            <p className="text-center text-gray-500 mb-8">Wprowadz swoje dane, aby sie zalogowac</p>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700" htmlFor="login">
                  Login
                </label>
                <div className="mt-1">
                  <input
                    id="login"
                    name="login"
                    type="text"
                    required
                    className="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
                    placeholder="Wprowadz login"
                    value={login}
                    onChange={(e) => setLogin(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700" htmlFor="password">
                  Haslo
                </label>
                <div className="mt-1">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    className="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-150 ease-in-out"
                    placeholder="Wprowadz haslo"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out disabled:opacity-50"
                >
                  {isLoading ? 'Logowanie...' : 'Zaloguj sie'}
                </button>
              </div>
            </form>
          </div>
          
          {/* Wyswietlanie komunikatu o statusie */}
          {statusMessage && (
            <div className={`p-4 border-t-4 transition-all duration-300 ease-in-out ${
              statusType === 'success' ? 'bg-green-50 border-green-500 text-green-800' :
              statusType === 'warning' ? 'bg-yellow-50 border-yellow-500 text-yellow-800' :
              'bg-red-100 border-red-600 text-red-900 shadow-[inset_0_0_20px_rgba(220,38,38,0.5)]'
            }`}>
              <div className="flex justify-center items-center">
                {statusType === 'error' && (
                  <svg className="h-6 w-6 text-red-600 mr-2 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                )}
                <span className={`text-center font-semibold ${statusType === 'error' ? 'text-lg uppercase tracking-wider' : ''}`}>
                  {statusMessage}
                </span>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;

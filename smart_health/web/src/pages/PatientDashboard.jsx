              {tokens.map(token => {
                const waitingTime = calculateWaitingTime(token);
                return (
                  <div
                    key={token._id}
                    className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-xl border border-green-100"
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex-1">
                        <p className="font-bold text-2xl text-green-600">
                          {token.tokenNumber}
                        </p>
                        <p className="text-gray-600">{token.department?.name}</p>
                        <p className="text-sm text-gray-500">
                          {new Date(token.createdAt).toLocaleDateString()}
                        </p>
                        <div className="mt-2">
                          <span className="text-sm font-semibold text-blue-600">
                            ⏱️ {token.status === 'completed' ? 'Total time: ' : 'Waiting: '}
                            {formatWaitingTime(waitingTime)}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-bold ${
                            token.status === 'called'
                              ? 'bg-yellow-100 text-yellow-800'
                              : token.status === 'waiting'
                              ? 'bg-blue-100 text-blue-800'
                              : token.status === 'completed'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {token.status}
                        </span>

                        {(token.status === 'waiting' || token.status === 'called') && (
                          <button
                            onClick={() => {
                              if (window.confirm('Are you sure you want to cancel this token?')) {
                                removeToken(token._id);
                              }
                            }}
                            className="bg-red-500 text-white px-2 py-1 rounded text-xs hover:bg-red-600 transition"
                            title="Cancel Token"
                          >
                            ✕
